import sys
import json
from ingest import run_ingestion
from analytics import run_analytics

def main():
    if len(sys.argv) < 2:
        print("use:")
        print("python main.py ingest")
        print("python main.py analytics")
        print("python main.py analytics 3  # top 3")
        return
    cmd = sys.argv[1].lower()
    if cmd == "ingest":
        result = run_ingestion()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "analytics":
        top_n = 5
        if len(sys.argv) >= 3:
            try:
                top_n = int(sys.argv[2])
                if top_n <= 0:
                    top_n = 5
            except ValueError:
                top_n = 5

        result = run_analytics(top_n=top_n)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Comando errado. Use:")
        print("python main.py ingest")
        print("python main.py analytics")
        print("python main.py analytics 3  # top 3")

if __name__ == "__main__":
    main()
