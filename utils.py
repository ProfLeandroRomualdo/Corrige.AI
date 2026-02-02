import oci

def call_llm(input):
    
    compartment_id = "ocid1......."
    CONFIG_PROFILE = "DEFAULT"
    config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

    # Service endpoint
    endpoint = "https://inference.generativeai.us-ashburn-1.oci.oraclecloud.com"

    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
    chat_detail = oci.generative_ai_inference.models.ChatDetails()

    content = oci.generative_ai_inference.models.TextContent()
    content.text = input
    message = oci.generative_ai_inference.models.Message()
    message.role = "USER"
    message.content = [content]

    chat_request = oci.generative_ai_inference.models.GenericChatRequest()
    chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
    chat_request.messages = [message]
    chat_request.max_tokens = 20000
    chat_request.temperature = 1

    chat_request.top_p = 1
    chat_request.top_k = 0

    chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id="ocid1.generativeaimodel.oc1.iad.amaaaaaask7dceyamqkpviarwzvo3wwuhnhqloa224fneaukac5megifuaba")
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = compartment_id

    response = generative_ai_inference_client.chat(chat_detail)

    if hasattr(response.data, "chat_response"):
        chat_resp = response.data.chat_response
        if hasattr(chat_resp, "text"):
            text_content: str = str(chat_resp.text)
            print("Successfully generated chat response")
        
        return chat_resp.choices[0].message.content[0].text