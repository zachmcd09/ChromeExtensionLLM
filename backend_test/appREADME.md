Implementation Breakdown                                               
                                                                                                                     
   1 Processing Chunks                                                                                               
      • The function iterates through chunks of text, processes each chunk for newline characters, and trims new     
        lines.                                                                                                       
   2 Server Request                                                                                                  
      • It sends a POST request to LMCLIENT (presumably the lmstudio server) with each chunk of text.                
   3 Response Handling                                                                                               
      • On receiving a response:                                                                                     
         • It checks if the status code is 200 (OK).                                                                 
         • Parses the JSON response to extract data. If 'data' is present and contains elements, it fetches the      
           first element assuming it holds the embedding.                                                            
         • It then checks for an 'embedding' key in this fetched data to return as a numpy array.                    
         • Raises exceptions if the 'embedding' key is missing or if the 'data' key is missing or invalid.           
      • Handles any other response error codes by raising an exception with the error message.   