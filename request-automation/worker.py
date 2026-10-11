import argparse
import json
import time
from workflow import Workflow

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='data/requests.db')
    parser.add_argument('--watch', action='store_true', help='Poll every second until Ctrl+C')
    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()
    flow = Workflow(args.db)
    if args.demo:
        job = flow.submit('demo-1', 'Urgent: login error during an outage')
    try:
        while True:
            processed = flow.run_one()
            if processed is not None:
                print(json.dumps(flow.get(processed), indent=2))
            elif not args.watch:
                break
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    if args.demo:
        print(json.dumps(flow.get(job), indent=2))
