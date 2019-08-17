import json
import logging 

import azure.functions as func

def prettijson(data):
    return json.dumps(data, indent=2, sort_keys=True, separators=(", ", " : "), check_circular=True)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    if req.method == "POST":
        logging.info("Handling POST web request")
        if req.headers["Content-Type"] != "application/json":
            logging.error("Request did not have proper Content-Type")
            return func.HttpResponse(
                "Content-Type header must be set to 'application/json'",
                status_code=400
            )
        
        logging.info("Attempting to prettify JSON")
        try:
            j = req.get_json()
            prettified_json = prettijson(j)
        except Exception as e:
            logging.error(f"Request was invalid JSON: {e}")
            return func.HttpResponse(
                "Request was invalid JSON",
                status_code=400
            )
        
        logging.info("Successfully prettified JSON")
        return func.HttpResponse(
            prettified_json,
            status_code=200
        )

    elif req.method == "OPTIONS":
        logging.info("Handling OPTIONS web request")
        return func.HttpResponse(
            json.dumps(["OPTIONS", "POST"]),
            status_code=200
        )

    else:
        logging.info("Rejecting other web request")
        return func.HttpResponse(
            f"HTTP Method {req.method} not allowed",
            status_code=400
        )

if __name__ == "__main__":
    main()