# Setup
Configure AWS profile with CLI, ensuring profile has access to Amazon Bedrock
# Run the program
By running 
python -m langraph_agent.run 
a sample ticket will be parsed into Langraph, and the appropriate action response will be produced. The response is ultimately grounded in the kb-documets, with it specifically referencing known-issues.md
# Questions Answered
There is one cycle in the langgraph, with the  "diagnose" node having two conditional routes, one which leads to the output node when it determines the result is grounded or when the bounded limit has been surpassed, and the other which leads to the reframe node. In the reframe node, we reframe the query with REFRAME_PROMPT

A possible question the user may ask that is not covered by our documents is: "what items are excluded from the refund policy?
