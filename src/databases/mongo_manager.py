from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from src.utils import get_logger
from datetime import datetime

logger = get_logger()
load_dotenv()
class MongoDB:
    def __init__(self):
        """Khởi tạo kết nối MongoDB với thông tin từ biến môi trường"""
        self.mongo_user = os.environ.get('MONGO_USER')
        self.mongo_pass = os.environ.get('MONGO_PASS')
        self.mongo_cluster = os.environ.get('MONGO_CLUSTER')
        
        if not all([self.mongo_user, self.mongo_pass, self.mongo_cluster]):
            raise ValueError("Missing required environment variables")
        
        # Tạo connection string
        self.connection_string = f"mongodb+srv://{self.mongo_user}:{self.mongo_pass}@info.fwj2z.mongodb.net/?retryWrites=true&w=majority&appName=Info"
        self.connection_string = f"mongodb+srv://{self.mongo_user}:{self.mongo_pass}@{self.mongo_cluster}.2uev0.mongodb.net/?retryWrites=true&w=majority&appName={self.mongo_cluster}"
        try:
            self.client = MongoClient(self.connection_string)
            self.database = self.client[self.mongo_cluster]
            # Kiểm tra kết nối
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def __enter__(self):
        """Context manager entry point"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - đóng kết nối"""
        self.close()

    def close(self):
        """Đóng kết nối MongoDB"""
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("MongoDB connection closed")

    def get_database(self):
        """Trả về đối tượng database"""
        return self.database

    def get_client(self):
        """Trả về đối tượng client"""
        return self.client

    def get_collection(self, collection_name: str):
        """Trả về collection được chỉ định"""
        return self.database[collection_name]

    # CREATE operations
    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """Thêm một document vào collection"""
        try:
            # Thêm timestamp
            document['created_at'] = datetime.now()
            document['updated_at'] = datetime.now()
            
            result = self.database[collection_name].insert_one(document)
            logger.info(f"Document inserted with id: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            return None

    def insert_many(self, collection_name: str, documents: List[Dict]) -> Optional[List[str]]:
        """Thêm nhiều documents vào collection"""
        try:
            # Thêm timestamp cho mỗi document
            for doc in documents:
                doc['created_at'] = datetime.now()
                doc['updated_at'] = datetime.now()
                
            result = self.database[collection_name].insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents")
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error inserting documents: {e}")
            return None

    # READ operations
    def find_one(self, collection_name: str, query: Dict, projection: Dict = None) -> Optional[Dict]:
        """Tìm một document theo điều kiện query"""
        try:
            return self.database[collection_name].find_one(query, projection)
        except Exception as e:
            logger.error(f"Error finding document: {e}")
            return None

    def find_many(self, collection_name: str, query: Dict, projection: Dict = None, 
                 sort: List = None, limit: int = None) -> List[Dict]:
        """Tìm nhiều documents theo điều kiện query với các tùy chọn sắp xếp và giới hạn"""
        try:
            cursor = self.database[collection_name].find(query, projection)
            
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
                
            return list(cursor)
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            return []

    # UPDATE operations
    def update_one(self, collection_name: str, query: Dict, update_data: Dict, 
                  upsert: bool = False) -> bool:
        """Cập nhật một document"""
        try:
            # Thêm timestamp cập nhật
            if '$set' in update_data:
                update_data['$set']['updated_at'] = datetime.now()
            else:
                update_data['$set'] = {'updated_at': datetime.now()}
                
            result = self.database[collection_name].update_one(
                query, update_data, upsert=upsert
            )
            logger.info(f"Modified {result.modified_count} document(s)")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return False

    def update_many(self, collection_name: str, query: Dict, update_data: Dict, 
                   upsert: bool = False) -> int:
        """Cập nhật nhiều documents"""
        try:
            # Thêm timestamp cập nhật
            if '$set' in update_data:
                update_data['$set']['updated_at'] = datetime.now()
            else:
                update_data['$set'] = {'updated_at': datetime.now()}
                
            result = self.database[collection_name].update_many(
                query, update_data, upsert=upsert
            )
            logger.info(f"Modified {result.modified_count} document(s)")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating documents: {e}")
            return 0

    # DELETE operations
    def delete_one(self, collection_name: str, query: Dict) -> bool:
        """Xóa một document"""
        try:
            result = self.database[collection_name].delete_one(query)
            logger.info(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

    def delete_many(self, collection_name: str, query: Dict) -> int:
        """Xóa nhiều documents"""
        try:
            result = self.database[collection_name].delete_many(query)
            logger.info(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return 0

    # Additional utility methods
    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """Đếm số lượng documents theo điều kiện query"""
        try:
            return self.database[collection_name].count_documents(query or {})
        except Exception as e:
            logger.error(f"Error counting documents: {e}")
            return 0

    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """Thực hiện aggregation pipeline"""
        try:
            return list(self.database[collection_name].aggregate(pipeline))
        except Exception as e:
            logger.error(f"Error in aggregation: {e}")
            return []

    def create_index(self, collection_name: str, keys: List[tuple], unique: bool = False):
        """Tạo index cho collection"""
        try:
            index_name = self.database[collection_name].create_index(keys, unique=unique)
            logger.info(f"Created index: {index_name}")
            return index_name
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return None
if __name__ == "__main__":
    db = MongoDB()
        
    