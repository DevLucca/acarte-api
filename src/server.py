from importlib import reload
import uvicorn
from core.settings import cfg

if __name__ == "__main__":
    uvicorn.run(
        "app:api",
        host="0.0.0.0",
        port=cfg.app_port.value if cfg.app_port.value else 4000,
        reload=True
    )
