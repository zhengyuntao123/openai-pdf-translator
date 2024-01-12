# V1.0 and V2.0
Implemented two translation methods.\
V1.0 involved pre-designing different prompts and translating through the OPENAI Chat Completion API\
V2.0 utilized chat_prompt_template in LangChain to construct prompts and LLMChain to achieve transalation functionality.

# How to use
Here are two examples.\
For V1.0: python ai_translator/main.py --model_type OpenAIModel --openai_api_key $OPENAI_API_KEY --file_format pdf\
For V2.0: python ai_translator/main.py --output_file_format pdf --input_file "tests/attention is all you need.pdf"\
More details can be checked in ai_translator/utils/argument_parser.py

# Examples
Examples can be seen in v1.0/tests and v2.0/tests
