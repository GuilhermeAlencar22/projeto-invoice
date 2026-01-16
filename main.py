import sys
import json
from ingest import run_ingestion
from analytics import run_analytics
def main():
    if len(sys.argv) < 2:
        print("use:")
        print("python main.py ingest")
        print("python main.py analytics")
        return

    cmd = sys.argv[1].lower()

    if cmd == "ingest":
        result = run_ingestion()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "analytics":
        result = run_analytics()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Comando errado")

if __name__ == "__main__":
    main()
