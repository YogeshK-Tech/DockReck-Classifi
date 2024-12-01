from sentence_transformers import SentenceTransformer
import pandas as pd

# model = SentenceTransformer('all-MiniLM-L6-v2')
#
# data_df = pd.DataFrame(columns=["File_Name", "Text", "Category", "Subcategory", "Embeddings"])
# cat_classifier = None
# subcat_classifier = None
# category_encoder = None
# subcategory_encoder = None

data_df = pd.DataFrame()
model = SentenceTransformer('all-MiniLM-L6-v2')
cat_classifier = None
subcat_classifier = None


# def load_data_from_files(folder_path):
#     """Load text files from a folder, extract labels from filenames, and encode content."""
#
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith(".txt"):
#             match = re.match(r"([^_]+)_([^_]+)\.txt", file_name)
#             if match:
#                 category, subcategory = match.groups()
#                 with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
#                     content = file.read().strip()
#                     embedding = global_config.model.encode(content)
#                     data_df = pd.concat([data_df, pd.DataFrame([[file_name, content, category, subcategory, embedding]],
#                                                                 columns=["File Name", "Text", "Category", "Subcategory", "Embeddings"])],
#                                         ignore_index=True)
#     print(f"Loaded {len(global_config.data_df)} documents.")