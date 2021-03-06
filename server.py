from src.core.settings import cfg
import uvicorn

if __name__ == "__main__":
    print(__name__)
    uvicorn.run(
        "src.app:api",
        host="0.0.0.0",
        port=cfg['app-port']['value'] if cfg['app-port']['value'] else 4000
    )
