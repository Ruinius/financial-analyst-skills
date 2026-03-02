"""
Tiger Transformer Server

A lightweight FastAPI server that hosts the tiger-transformer model (fine-tuned FINBERT)
for standardizing financial statement line items. This allows skills to perform 
inference quickly without reloading the model for every call.
"""

import os
import csv
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tiger-transformer-server")

app = FastAPI(title="Tiger Transformer Server", version="1.0.0")

# --- Models & Configuration ---

class LineItem(BaseModel):
    line_name: str
    line_category: str
    line_order: Optional[int] = 0

class PredictionRequest(BaseModel):
    items: List[LineItem]

class PredictionResponse(BaseModel):
    standardized_name: str
    is_calculated: Optional[bool] = None
    is_operating: Optional[bool] = None
    is_expense: Optional[bool] = None
    confidence: float

# --- Global State ---

class TigerTransformerState:
    model = None
    tokenizer = None
    bs_mapping = {}
    is_mapping = {}

state = TigerTransformerState()

# --- Initialization ---

def load_mappings():
    """Load the CSV mapping files from the tools directory."""
    tools_dir = Path(__file__).parent
    
    # Load balance sheet mapping
    bs_path = tools_dir / "bs_calculated_operating_mapping.csv"
    if bs_path.exists():
        with open(bs_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                state.bs_mapping[row["standardized_name"]] = {
                    "is_calculated": row["is_calculated"].lower() == "true",
                    "is_operating": row["is_operating"].lower() == "true" if row["is_operating"] else None
                }
        logger.info(f"Loaded {len(state.bs_mapping)} balance sheet mappings")
    else:
        logger.warning(f"Balance sheet mapping not found at {bs_path}")

    # Load income statement mapping
    is_path = tools_dir / "is_calculated_operating_expense_mapping.csv"
    if is_path.exists():
        with open(is_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                state.is_mapping[row["standardized_name"]] = {
                    "is_calculated": row["is_calculated"].lower() == "true",
                    "is_operating": row["is_operating"].lower() == "true" if row["is_operating"] else None,
                    "is_expense": row["is_expense"].lower() == "true" if row["is_expense"] else None,
                }
        logger.info(f"Loaded {len(state.is_mapping)} income statement mappings")
    else:
        logger.warning(f"Income statement mapping not found at {is_path}")

def load_model():
    """Load the FINBERT model and tokenizer."""
    # Path to tiger-transformer/models - can be overridden via environment variable
    default_base = Path("F:/AIML projects/tiger-transformer")
    base_dir = Path(os.getenv("TIGER_TRANSFORMER_PATH", str(default_base)))
    
    model_dir = base_dir / "models" / "financial_transformer"
    label_map_path = base_dir / "models" / "label_map.json"

    if not model_dir.exists():
        raise RuntimeError(f"Model directory not found: {model_dir}")

    logger.info(f"Loading model from {model_dir}...")
    state.tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    state.model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))

    # Load label mapping
    if label_map_path.exists():
        with open(label_map_path, encoding="utf-8") as f:
            label2id = json.load(f)
        id2label = {int(v): k for k, v in label2id.items()}
        state.model.config.id2label = id2label
        state.model.config.label2id = label2id
        logger.info(f"Loaded label map with {len(id2label)} entries")

    # GPU Check
    device = "cuda" if torch.cuda.is_available() else "cpu"
    state.model = state.model.to(device)
    state.model.eval()
    logger.info(f"Model loaded successfully on {device}")

@app.on_event("startup")
def startup_event():
    load_mappings()
    try:
        load_model()
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # We don't exit here so the server can still run/health check can fail
        # But predictions will fail

# --- Inference Logic ---

def batch_inference(inputs: List[str]) -> List[Dict[str, Any]]:
    """Run batch inference on a list of formatted input strings."""
    if not state.model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    encoded = state.tokenizer(
        inputs, padding=True, truncation=True, max_length=512, return_tensors="pt"
    )
    
    device = next(state.model.parameters()).device
    encoded = {k: v.to(device) for k, v in encoded.items()}

    with torch.no_grad():
        outputs = state.model(**encoded)
        probs = torch.softmax(outputs.logits, dim=-1)
        confidences, predictions = torch.max(probs, dim=-1)

    results = []
    for pred, conf in zip(predictions, confidences):
        results.append({
            "standardized_name": state.model.config.id2label[pred.item()],
            "confidence": float(conf.item())
        })
    return results

# --- Endpoints ---

@app.get("/health")
def health():
    return {
        "status": "ready" if state.model else "initializing",
        "device": str(next(state.model.parameters()).device) if state.model else "n/a",
        "mappings": {
            "bs": len(state.bs_mapping),
            "is": len(state.is_mapping)
        }
    }

@app.post("/predict/balance-sheet", response_model=List[PredictionResponse])
def predict_bs(request: PredictionRequest):
    items = request.items
    if not items:
        return []

    # Format inputs: [PREV_2] [PREV_1] [SECTION] [RAW_NAME] [NEXT_1] [NEXT_2]
    inputs = []
    for i, item in enumerate(items):
        prev_2 = items[i - 2].line_name if i >= 2 else "<START>"
        prev_1 = items[i - 1].line_name if i >= 1 else "<START>"
        next_1 = items[i + 1].line_name if i < len(items) - 1 else "<END>"
        next_2 = items[i + 2].line_name if i < len(items) - 2 else "<END>"

        input_text = (
            f"[{prev_2}] [{prev_1}] [{item.line_category}] "
            f"[{item.line_name}] [{next_1}] [{next_2}]"
        )
        inputs.append(input_text)

    predictions = batch_inference(inputs)
    
    # Enrich with mapping data
    results = []
    for pred in predictions:
        std_name = pred["standardized_name"]
        mapping = state.bs_mapping.get(std_name, {})
        results.append({
            **pred,
            "is_calculated": mapping.get("is_calculated"),
            "is_operating": mapping.get("is_operating")
        })
    return results

@app.post("/predict/income-statement", response_model=List[PredictionResponse])
def predict_is(request: PredictionRequest):
    items = request.items
    if not items:
        return []

    inputs = []
    for i, item in enumerate(items):
        prev_2 = items[i - 2].line_name if i >= 2 else "<START>"
        prev_1 = items[i - 1].line_name if i >= 1 else "<START>"
        next_1 = items[i + 1].line_name if i < len(items) - 1 else "<END>"
        next_2 = items[i + 2].line_name if i < len(items) - 2 else "<END>"

        input_text = (
            f"[{prev_2}] [{prev_1}] [{item.line_category}] "
            f"[{item.line_name}] [{next_1}] [{next_2}]"
        )
        inputs.append(input_text)

    predictions = batch_inference(inputs)
    
    results = []
    for pred in predictions:
        std_name = pred["standardized_name"]
        mapping = state.is_mapping.get(std_name, {})
        results.append({
            **pred,
            "is_calculated": mapping.get("is_calculated"),
            "is_operating": mapping.get("is_operating"),
            "is_expense": mapping.get("is_expense"),
        })
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
