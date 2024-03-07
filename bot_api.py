from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import dialogflow_v2 as dialogflow

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Retrieve incoming message from WhatsApp
    user_message = request.values.get("Body")

    # Process the message using Dialogflow
    dialogflow_response = get_dialogflow_response(user_message)

    # Send the Dialogflow response back to WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(dialogflow_response)
    return str(twilio_response)
def get_dialogflow_response(user_message):
    # Set up Dialogflow client
    project_id = "your-dialogflow-project-id"
    session_id = "whatsapp-bot-session-id"
    language_code = "en-US"

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    # Send user message to Dialogflow
    text_input = dialogflow.TextInput(text=user_message, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    # Get Dialogflow's response
    return response.query_result.fulfillment_text

if __name__ == "__main__":
    app.run(debug=True)
