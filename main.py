from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TradeInput(BaseModel):
    setup: str
    entry: float
    exit: float
    stop_loss: Optional[float] = None
    emotion: Optional[str] = None
    mistake: Optional[str] = None

class TradeAnalysis(BaseModel):
    setup_score: int
    discipline_score: int
    insights: List[str]
    suggestions: List[str]

def analyze_logic(data):
    insights = []
    suggestions = []

    pnl = data.exit - data.entry

    if data.emotion == "fomo" or data.mistake == "late_entry":
        insights.append("FOMO or late entry detected")
        suggestions.append("Avoid chasing trades, wait for confirmation")

    if pnl < 0:
        insights.append("Loss trade detected")
        suggestions.append("Improve entry timing")

    if data.stop_loss is None:
        insights.append("No stop loss used")
        suggestions.append("Always define risk")

    score = max(1, 10 - len(insights))

    return score, insights, suggestions

@app.post("/api/v1/analyze-trade", response_model=TradeAnalysis)
def analyze_trade(data: TradeInput):
    score, insights, suggestions = analyze_logic(data)

    return {
        "setup_score": score,
        "discipline_score": score,
        "insights": insights or ["No major issues"],
        "suggestions": suggestions or ["Keep following your strategy"]
    }