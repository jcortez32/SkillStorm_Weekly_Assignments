# Info 
The agentcore system investigates clinic appoitnments and handles rescheduling appointments. The system requires appointment ids to investigate. A seeded appointment has been filled in with id "20260810"
# Setup
1. Configure Aws profile to allow for comprehend:DetectPiiEntities, bedrock:ApplyGuardrail, and InvokeBedrock 
2. Run Agentcore project locally via agentcore dev

# What would I do with more time
Due to difficulties with getting the agentcore setup initially and configuring the tools properly, I did not get to fully implement the guardrails with our control commands. I have the guardrails setup in AWS and tentively have it configured to our entire model to test that it works but they are not binded. With more time i would actually implement the tools and create the key tests
