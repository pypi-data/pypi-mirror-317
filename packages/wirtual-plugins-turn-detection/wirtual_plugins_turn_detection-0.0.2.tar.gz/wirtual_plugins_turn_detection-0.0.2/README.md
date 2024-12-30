## Installation

```bash
pip install wirtual-plugins-turn-detection
```

## Usage

This plugin is designed to be used with the `WirtualPipelineAgent`:

```python
from wirtual.plugins import turn_detector

agent = WirtualPipelineAgent(
    ...
    turn_detector=turn_detector.EOUModel(),
)
```

## Running your agent

This plugin requires model files. Before starting your agent for the first time, or when building Docker images for deployment, run the following command to download the model files:

```bash
python wirtual_agent.py download-files
```