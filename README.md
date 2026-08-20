# Pepkio pI Charge Consensus

Python client for the Pepkio `pi-charge-consensus` tool.

## Installation

```bash
pip install pepkio-pi-charge-consensus
```

## Quick Start

```python
from pepkio_pi_charge_consensus import PepkioClient

with PepkioClient() as client:
    example_input = client.get_example_input("lysozyme_single")
    result = client.run(example_input)
    print("Status:", result.status)
    print("Result:", result.result)
```
