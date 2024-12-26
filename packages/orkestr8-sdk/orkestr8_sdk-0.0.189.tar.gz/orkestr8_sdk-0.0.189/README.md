# orkestr8-sdk

Python SDK to simplify resource accumulation and model training. This SDK is used by Orkestr8-ML.

## Testing

The venv needs to be manually invoked. Poetry is only used as a dep resolver
1. `venv/scripts/activate`: Active local venv
2. `make test`

## Development

Run this command to automatically create a new version

```
make tag version=v0.0.178 message="'your message. Notice the double quotes'"
```
