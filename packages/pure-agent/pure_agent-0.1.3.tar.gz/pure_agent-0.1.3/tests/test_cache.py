import os
from pure_agent import LocalCache, pretty_print_nested

dir_path = '.cache'

# Create a cache instance
cache = LocalCache(dir_path)

if not os.path.isdir(dir_path):
    # Set a cache entry with expiration
    cache.set('username', 'Alice', expire=3600)  # Expires in 1 hour

    # Get a cache entry
    username = cache.get('username')
    print(f"Username: {username}")  # Output: Username: Alice

    # Check if a key exists
    print(f"Exists: {cache.exists('username')}")  # Output: Exists: True

    # Delete a cache entry
    cache.delete('username')
    print(f"Exists after delete: {cache.exists('username')}")  # Output: Exists after delete: False

    # Clear all cache entries
    cache.clear()
else:
    print(pretty_print_nested(cache.items_dict()))
    cache.to_json('cache.json')
