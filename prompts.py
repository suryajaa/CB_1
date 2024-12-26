from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate, PromptTemplate

# Example prompt template: Maps input questions to their SQL queries
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),  # User question
        ("ai", "{query}"),               # Corresponding SQL query
    ]
)

# Few-shot learning prompt template with dynamically selected examples
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),  # Selects the most relevant examples
    input_variables=["input"],                # Input variables used in the template
)

# Final prompt template for generating SQL queries
final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. "
            "Unless otherwise specified.\n\nHere is the relevant table info: {table_info}\n\n"
            "Below are a number of examples of questions and their corresponding SQL queries."
        ),
        few_shot_prompt,                          # Include dynamically selected examples
        MessagesPlaceholder(variable_name="messages"),  # Placeholder for chat history
        ("human", "{input}"),                     # User's input question
    ]
)

# Answer prompt for interpreting SQL results
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)
