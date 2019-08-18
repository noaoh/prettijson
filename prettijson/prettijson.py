import json
import logging 

import azure.functions as func

def prettijson(data):
    seps = (", ", " : ")
    return (
        json.dumps(data, indent=2, sort_keys=True, separators=seps) + "\n"
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request\n")
    if req.method == "POST":
        logging.info("Handling POST web request")
        if req.headers["Content-Type"] != "application/json":
            logging.error("Request did not have proper Content-Type")
            return func.HttpResponse(
                "Content-Type header must be set to 'application/json'\n",
                status_code=400
            )
        
        logging.info("Attempting to prettify JSON\n")
        try:
            j = req.get_json()
            prettified_json = prettijson(j)
        except Exception as e:
            logging.error(f"Request was invalid JSON: {e}\n"])
            return func.HttpResponse(
                "Request was invalid JSON\n",
                status_code=400
            )
        
        logging.info("Successfully prettified JSON\n")
        return func.HttpResponse(
            prettified_json,
            status_code=200
        )

    elif req.method == "OPTIONS":
        logging.info("Handling OPTIONS web request\n")
        return func.HttpResponse(
            json.dumps(["OPTIONS", "POST"]),
            status_code=200
        )

    else:
        logging.info("Rejecting other web request\n")
        return func.HttpResponse(
            f"HTTP Method {req.method} not allowed\n",
            status_code=400
        )

if __name__ == "__main__":
    main()

