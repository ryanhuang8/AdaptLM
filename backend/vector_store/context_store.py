# """
# Context-Aware Vector Store for LLM systems with automatic metadata management.
# """

# import uuid
# from datetime import datetime
# from typing import List, Dict, Any, Optional
# from .vector_store import PineconeVectorStore


# class ContextAwareVectorStore:
#     """
#     Context-Aware Vector Store that automatically manages metadata for LLM context.
#     Handles user sessions, model switching, and conversation tracking seamlessly.
#     """
    
#     def __init__(self, index_name: str = "contextllm-context-index"):
#         """
#         Initialize Context-Aware Vector Store.
        
#         Args:
#             index_name: Name of the Pinecone index for context storage
#         """
#         self.vector_store = PineconeVectorStore(index_name=index_name)
    
#     def store_context(self, 
#                      text: str, 
#                      user_id: str, 
#                      session_id: str,
#                      llm_model: str, 
#                      conversation_id: str,
#                      content_role: str = "user_message",
#                      context_type: str = "conversation",
#                      timestamp: Optional[str] = None,
#                      additional_metadata: Optional[Dict[str, Any]] = None) -> str:
#         """
#         Store context with automatically generated metadata.
        
#         Args:
#             text: The text content to store
#             user_id: Unique identifier for the user
#             session_id: Session identifier
#             llm_model: Name of the LLM model (e.g., "gpt-4", "claude", "gemini")
#             conversation_id: Unique conversation identifier
#             content_role: Role of the content ("user_message", "assistant_response", "system_prompt")
#             context_type: Type of context ("conversation", "document", "knowledge")
#             timestamp: ISO timestamp (auto-generated if None)
#             additional_metadata: Any additional metadata to include
            
#         Returns:
#             Vector ID of the stored context
#         """
#         if timestamp is None:
#             timestamp = datetime.now().isoformat()
        
#         # Generate vector ID
#         vector_id = str(uuid.uuid4())
        
#         # Build metadata
#         metadata = {
#             # Core content
#             "text": text,
            
#             # User identification
#             "user_id": user_id,
#             "session_id": session_id,
            
#             # LLM context
#             "llm_model": llm_model,
#             "conversation_id": conversation_id,
            
#             # Temporal context
#             "timestamp": timestamp,
            
#             # Content classification
#             "context_type": context_type,
#             "content_role": content_role,
            
#             # Technical tracking
#             "vector_id": vector_id,
#             "embedding_model": self.vector_store.model_name
#         }
        
#         # Add any additional metadata
#         if additional_metadata:
#             metadata.update(additional_metadata)
        
#         # Store in vector database
#         vector_ids = self.vector_store.upsert_texts([text], [metadata])
#         return vector_ids[0] if vector_ids else None
    
#     def retrieve_context(self, 
#                         user_id: str,
#                         query_text: Optional[str] = None,
#                         session_id: Optional[str] = None,
#                         llm_model: Optional[str] = None,
#                         conversation_id: Optional[str] = None,
#                         context_type: Optional[str] = None,
#                         content_role: Optional[str] = None,
#                         top_k: int = 10,
#                         include_metadata: bool = True) -> List[Dict[str, Any]]:
#         """
#         Retrieve relevant context based on filters and similarity.
        
#         Args:
#             user_id: User identifier (required)
#             query_text: Text to search for similarity (if None, uses filters only)
#             session_id: Filter by session
#             llm_model: Filter by LLM model
#             conversation_id: Filter by conversation
#             context_type: Filter by context type
#             content_role: Filter by content role
#             top_k: Number of results to return
#             include_metadata: Whether to include metadata in results
            
#         Returns:
#             List of context entries with scores and metadata
#         """
#         # Build filter dictionary
#         filter_dict = {"user_id": user_id}
        
#         if session_id:
#             filter_dict["session_id"] = session_id
#         if llm_model:
#             filter_dict["llm_model"] = llm_model
#         if conversation_id:
#             filter_dict["conversation_id"] = conversation_id
#         if context_type:
#             filter_dict["context_type"] = context_type
#         if content_role:
#             filter_dict["content_role"] = content_role
        
#         # If no query text, use empty string for filter-only search
#         if query_text is None:
#             query_text = ""
        
#         # Query the vector store
#         results = self.vector_store.query(
#             query_text=query_text,
#             top_k=top_k,
#             filter_dict=filter_dict
#         )
        
#         return results
    
#     def get_conversation_history(self, 
#                                 user_id: str,
#                                 conversation_id: str,
#                                 llm_model: Optional[str] = None,
#                                 limit: int = 50) -> List[Dict[str, Any]]:
#         """
#         Get chronological conversation history for a specific conversation.
        
#         Args:
#             user_id: User identifier
#             conversation_id: Conversation identifier
#             llm_model: Optional model filter
#             limit: Maximum number of messages to return
            
#         Returns:
#             List of conversation messages in chronological order
#         """
#         filter_dict = {
#             "user_id": user_id,
#             "conversation_id": conversation_id,
#             "context_type": "conversation"
#         }
        
#         if llm_model:
#             filter_dict["llm_model"] = llm_model
        
#         # Get all messages for this conversation
#         results = self.vector_store.query(
#             query_text="",
#             top_k=limit,
#             filter_dict=filter_dict
#         )
        
#         # Sort by timestamp
#         sorted_results = sorted(
#             results, 
#             key=lambda x: x["metadata"]["timestamp"]
#         )
        
#         return sorted_results
    
#     def switch_llm_context(self, 
#                           user_id: str,
#                           session_id: str,
#                           old_model: str,
#                           new_model: str,
#                           conversation_id: Optional[str] = None) -> bool:
#         """
#         Switch context from one LLM model to another.
        
#         Args:
#             user_id: User identifier
#             session_id: Session identifier
#             old_model: Previous LLM model
#             new_model: New LLM model
#             conversation_id: Optional conversation to switch
            
#         Returns:
#             True if successful
#         """
#         try:
#             # Get context from old model
#             filter_dict = {
#                 "user_id": user_id,
#                 "session_id": session_id,
#                 "llm_model": old_model
#             }
            
#             if conversation_id:
#                 filter_dict["conversation_id"] = conversation_id
            
#             old_context = self.vector_store.query(
#                 query_text="",
#                 top_k=100,  # Get all context
#                 filter_dict=filter_dict
#             )
            
#             # Store context with new model
#             for ctx in old_context:
#                 metadata = ctx["metadata"]
#                 self.store_context(
#                     text=metadata["text"],
#                     user_id=user_id,
#                     session_id=session_id,
#                     llm_model=new_model,
#                     conversation_id=metadata["conversation_id"],
#                     content_role=metadata["content_role"],
#                     context_type=metadata["context_type"],
#                     timestamp=metadata["timestamp"]
#                 )
            
#             return True
            
#         except Exception as e:
#             print(f"Error switching LLM context: {e}")
#             return False
    
#     def cleanup_expired_context(self, 
#                                user_id: Optional[str] = None,
#                                days_old: int = 30) -> int:
#         """
#         Clean up old context entries.
        
#         Args:
#             user_id: Optional user filter
#             days_old: Delete context older than this many days
            
#         Returns:
#             Number of deleted entries
#         """
#         cutoff_date = datetime.now().replace(
#             day=datetime.now().day - days_old
#         ).isoformat()
        
#         filter_dict = {
#             "timestamp": {"$lt": cutoff_date}
#         }
        
#         if user_id:
#             filter_dict["user_id"] = user_id
        
#         # Get expired entries
#         expired = self.vector_store.query(
#             query_text="",
#             top_k=1000,  # Large number to get all expired
#             filter_dict=filter_dict
#         )
        
#         # Delete expired entries
#         deleted_count = 0
#         for entry in expired:
#             try:
#                 self.vector_store.delete([entry["id"]])
#                 deleted_count += 1
#             except Exception as e:
#                 print(f"Error deleting expired entry {entry['id']}: {e}")
        
#         return deleted_count
    
#     def get_user_stats(self, user_id: str) -> Dict[str, Any]:
#         """
#         Get statistics for a specific user.
        
#         Args:
#             user_id: User identifier
            
#         Returns:
#             Dictionary with user statistics
#         """
#         # Get all user context
#         user_context = self.vector_store.query(
#             query_text="",
#             top_k=1000,
#             filter_dict={"user_id": user_id}
#         )
        
#         # Calculate statistics
#         stats = {
#             "total_context_entries": len(user_context),
#             "models_used": set(),
#             "conversations": set(),
#             "sessions": set(),
#             "context_types": {},
#             "content_roles": {}
#         }
        
#         for ctx in user_context:
#             metadata = ctx["metadata"]
#             stats["models_used"].add(metadata["llm_model"])
#             stats["conversations"].add(metadata["conversation_id"])
#             stats["sessions"].add(metadata["session_id"])
            
#             # Count context types
#             context_type = metadata["context_type"]
#             stats["context_types"][context_type] = stats["context_types"].get(context_type, 0) + 1
            
#             # Count content roles
#             content_role = metadata["content_role"]
#             stats["content_roles"][content_role] = stats["content_roles"].get(content_role, 0) + 1
        
#         # Convert sets to lists for JSON serialization
#         stats["models_used"] = list(stats["models_used"])
#         stats["conversations"] = list(stats["conversations"])
#         stats["sessions"] = list(stats["sessions"])
        
#         return stats
    
#     def delete_user_context(self, user_id: str) -> bool:
#         """
#         Delete all context for a specific user.
        
#         Args:
#             user_id: User identifier
            
#         Returns:
#             True if successful
#         """
#         try:
#             # Get all user context
#             user_context = self.vector_store.query(
#                 query_text="",
#                 top_k=10000,  # Large number to get all
#                 filter_dict={"user_id": user_id}
#             )
            
#             # Delete all entries
#             vector_ids = [ctx["id"] for ctx in user_context]
#             if vector_ids:
#                 self.vector_store.delete(vector_ids)
            
#             return True
            
#         except Exception as e:
#             print(f"Error deleting user context: {e}")
#             return False 