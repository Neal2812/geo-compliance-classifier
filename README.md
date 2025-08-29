# Confidence Validator Agent for Compliance Predictions

A robust ensemble system that ensures reliable compliance predictions by cross-validating outputs from multiple specialized models.

## 🎯 Overview

The Confidence Validator Agent acts as a "confidence validator" that cross-validates compliance predictions from three different models to ensure reliability and reduce false positives/negatives. It implements sophisticated ensemble logic to aggregate decisions and automatically approve high-confidence unanimous cases while flagging uncertain ones for manual review.

## 🏗️ Architecture

### Model Ensemble

| Model | Type | Base | Strength |
|-------|------|------|----------|
| **Legal-BERT Fine-tuned** | Primary | `nlpaueb/legal-bert-base-uncased` | Specialized legal language comprehension |
| **Rules-Based Classifier** | Hybrid | Pattern matching + rule triggers | Interpretable and reliable on clear-cut cases |
| **General-Purpose LLM + RAG** | Context-Enhanced | GPT-4/Claude + regulatory database | Handles novel or edge-case scenarios |

### Decision Schema

All models output standardized decisions:
- **Compliant** - Text indicates compliance with regulations
- **Non-Compliant** - Text indicates non-compliance or violations  
- **Unclear** - Compliance status is ambiguous or unclear

## 🚀 Features

### Core Functionality
- **Multi-Model Validation** - Collects predictions from all three models
- **Ensemble Logic** - Applies sophisticated aggregation algorithms
- **Auto-Approval** - Automatically approves high-confidence unanimous decisions
- **Manual Review Flagging** - Flags cases requiring human oversight
- **Transparency** - Provides detailed reasoning and traceability

### Ensemble Logic
1. **Unanimous Agreement** - If all models agree with confidence > 0.85, auto-approve
2. **Majority Vote** - If 2+ models agree, use majority decision with confidence aggregation
3. **Tiebreaker** - Use Legal-BERT as domain-specific tiebreaker when no clear majority
4. **Low Confidence** - Flag for manual review if average confidence < 0.85

### Output Format
Returns results in structured markdown tables with columns:
- Case ID
- Legal-BERT Decision (Confidence)
- Rules-Based Decision (Confidence)  
- LLM+RAG Decision (Confidence)
- Final Ensemble Decision
- Notes/Flags

## 📦 Installation

### Prerequisites
- Python 3.8+
- PyTorch (for Legal-BERT)
- OpenAI API key (for LLM+RAG model)

### Setup
```bash
# Clone repository
git clone <repository-url>
cd geo-compliance-classifier

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (optional, for LLM+RAG model)
export OPENAI_API_KEY="your-api-key-here"
```

## 🧪 Usage

### Basic Usage

```python
from src.confidence_validator import ConfidenceValidatorAgent

# Initialize the validator
validator = ConfidenceValidatorAgent(openai_api_key="your-key")

# Validate a compliance case
result = validator.validate_case(
    text="The organization maintains full compliance with data protection regulations.",
    case_id="CASE-001"
)

# Access results
print(f"Decision: {result.ensemble_decision}")
print(f"Confidence: {result.ensemble_confidence}")
print(f"Auto-Approved: {result.auto_approved}")
```

### Demo Script

Run the included demo to see the system in action:

```bash
python demo_confidence_validator.py
```

### Batch Processing

```python
# Process multiple cases
cases = [
    "Text 1...",
    "Text 2...",
    "Text 3..."
]

for i, case_text in enumerate(cases):
    result = validator.validate_case(case_text, f"CASE-{i+1:03d}")

# Get summary
summary_df = validator.get_validation_summary()
print(summary_df)

# Export to markdown
markdown_file = validator.export_results_markdown()
```

## 🔧 Configuration

### Confidence Thresholds
```python
validator = ConfidenceValidatorAgent()
validator.confidence_threshold = 0.85      # Minimum confidence for consideration
validator.auto_approval_threshold = 0.85   # Minimum confidence for auto-approval
```

### Model Customization
```python
# Custom Legal-BERT model path
from src.models.legal_bert_model import LegalBERTModel
custom_bert = LegalBERTModel("path/to/custom/model")

# Custom LLM model
from src.models.llm_rag_model import LLMRAGModel
custom_llm = LLMRAGModel(api_key="key", model="gpt-4-turbo")
```

## 📊 Output Examples

### Auto-Approved Case
```
Case ID: CASE-001
✅ Final Decision: Compliant (Confidence: 0.92)
🔄 Auto-Approved: Yes
🤝 Agreement Level: Unanimous

Model Predictions:
  ✅ Legal-BERT: Compliant (0.95)
  ✅ Rules-Based: Compliant (0.90)
  ✅ LLM+RAG: Compliant (0.92)
```

### Manual Review Required
```
Case ID: CASE-002
⚠️ Final Decision: Non-Compliant (Confidence: 0.78)
🔄 Auto-Approved: No
🤝 Agreement Level: Majority

Model Predictions:
  ✅ Legal-BERT: Non-Compliant (0.85)
  ✅ Rules-Based: Non-Compliant (0.80)
  ⚠️ LLM+RAG: Unclear (0.70)

🚩 Flags:
  - Low confidence despite majority agreement
```

## 🎛️ Advanced Features

### Model Reasoning
```python
# Get detailed reasoning from models
for model_name, prediction in result.predictions.items():
    print(f"{model_name}: {prediction.reasoning}")
```

### Model Status
```python
# Check model health and status
status = validator.get_model_status()
for model_name, info in status.items():
    print(f"{model_name}: {info['status']}")
```

### Custom Rules
```python
# Add custom compliance rules to Rules-Based Classifier
from src.models.rules_based_classifier import RulesBasedClassifier

classifier = RulesBasedClassifier()
# Add custom rules as needed
```

## 🔍 Validation Logic Details

### Stop Conditions
Task is complete when:
1. Three models have been run on the same case
2. Their outputs have been compared and analyzed
3. High-confidence unanimous decisions are auto-approved
4. Any disagreements/low-confidence cases are flagged with reasoning

### Priority Logic
- **Legal-BERT Priority**: Used as tiebreaker due to domain expertise
- **Confidence Aggregation**: Weighted by model agreement levels
- **Fallback Handling**: Graceful degradation when models fail

## 🚨 Error Handling

The system includes robust error handling:
- **Model Failures**: Automatic fallback to keyword-based classification
- **API Errors**: Graceful degradation for external service failures
- **Invalid Inputs**: Input validation and sanitization
- **Partial Failures**: Continue processing with available models

## 📈 Performance Considerations

### Optimization Tips
- **Batch Processing**: Process multiple cases together for efficiency
- **Model Caching**: Models are loaded once and reused
- **Async Processing**: Consider async for high-volume scenarios
- **Memory Management**: Large models are loaded on-demand

### Scalability
- **Horizontal Scaling**: Deploy multiple validator instances
- **Model Distribution**: Distribute models across different machines
- **Queue Systems**: Use message queues for high-throughput processing

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Code formatting
black src/
flake8 src/
```

### Adding New Models
1. Create model class in `src/models/`
2. Implement `predict()` and `get_model_info()` methods
3. Add to `src/models/__init__.py`
4. Update `ConfidenceValidatorAgent` to include new model

## 📝 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the demo script for usage examples
2. Review model status and error logs
3. Ensure all dependencies are properly installed
4. Verify API keys and model access

---

**Note**: This system is designed for compliance validation and should be used in conjunction with human oversight for critical decisions. The auto-approval feature is intended to reduce manual review burden for clear-cut cases, but all flagged cases should receive appropriate human review.
