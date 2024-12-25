from .vasrch import VaSrch

# Create an instance of the VaSrch class to expose its methods as module-level functions
_vasrch_instance = VaSrch()

# Expose the methods of the VaSrch class as module-level functions
extract_features = _vasrch_instance.extract_features
get_optimal_num_clusters = _vasrch_instance.get_optimal_num_clusters
train_clusters = _vasrch_instance.train_clusters
search_similar_images = _vasrch_instance.search_similar_images
