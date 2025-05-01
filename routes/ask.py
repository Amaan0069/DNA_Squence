@app.post("/ask-me-anything/")
async def ask_me_anything(data: AskRequest):
    # Log the incoming question
    logger.info(f"Received question: {data.question}")
    
    # Check if we have any data loaded
    if not uploaded_data:
        return {"answer": "No data has been uploaded yet. Please upload a CSV file first."}
    
    # Simple data analysis based on keywords in the question
    question_lower = data.question.lower()
    
    # Check if the question is about average age
    if "average" in question_lower and "age" in question_lower:
        try:
            # Calculate average age from the uploaded data
            ages = [entry["age"] for entry in uploaded_data if "age" in entry]
            if not ages:
                return {"answer": "I couldn't find age data in the uploaded information."}
            
            average_age = sum(ages) / len(ages)
            return {"answer": f"The average age in the uploaded data is {average_age:.2f} years."}
        except Exception as e:
            logger.error(f"Error calculating average age: {str(e)}")
            return {"answer": f"I encountered an error while calculating the average age: {str(e)}"}
    
    # Check if the question is about regions
    elif "region" in question_lower or "regions" in question_lower:
        try:
            # Get list of regions from the uploaded data
            regions = [entry["region"] for entry in uploaded_data if "region" in entry]
            regions_count = {}
            for region in regions:
                regions_count[region] = regions_count.get(region, 0) + 1
                
            region_info = ", ".join([f"{region}: {count}" for region, count in regions_count.items()])
            return {"answer": f"The data includes the following regions: {region_info}"}
        except Exception as e:
            logger.error(f"Error analyzing regions: {str(e)}")
            return {"answer": f"I encountered an error while analyzing regions: {str(e)}"}
    
    # Check if the question is about count/number of records
    elif any(word in question_lower for word in ["many", "count", "number", "records", "samples"]):
        return {"answer": f"There are {len(uploaded_data)} records in the uploaded data."}
    
    # If we can't determine what the question is about, use the Gemini API if available
    elif GEMINI_API_KEY:
        try:
            # Prepare context from our uploaded data (limit to first 10 records to avoid token limits)
            data_context = "Based on the following data:\n"
            for sample_id, details in enumerate(uploaded_data[:10]):
                data_context += f"ID: {sample_id+1}, Region: {details.get('region', 'Unknown')}, Age: {details.get('age', 'Unknown')}, Seed: {details.get('seed', 'Unknown')}\n"
            
            # Prepare the question with context
            augmented_question = f"{data_context}\n\nQuestion: {data.question}"
            
            # Call the Gemini API with the context-augmented question
            url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
            
            headers = {
                "Content-Type": "application/json",
            }
            
            params = {
                "key": GEMINI_API_KEY
            }
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": augmented_question
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 200,
                    "topP": 0.95,
                    "topK": 40
                }
            }
            
            response = requests.post(url, headers=headers, params=params, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                try:
                    answer = response_data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    answer = "Sorry, I couldn't process the response from the AI model."
            else:
                logger.error(f"API Error: {response.status_code}, {response.text}")
                return {"answer": f"Error: {response.status_code}. The API couldn't process your request."}
            
            return {"answer": answer}
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return {"answer": f"I encountered an error: {str(e)}"}
    else:
        return {"answer": "I'm sorry, I don't have enough information to answer that question. Please try asking about the age, region, or number of records in the uploaded data."}