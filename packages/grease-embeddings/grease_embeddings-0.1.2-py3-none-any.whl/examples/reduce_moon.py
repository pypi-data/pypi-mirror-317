from examples.data import load_data
from src.grease import GrEASE
import torch
import matplotlib.pyplot as plt


x_train, x_test, y_train, y_test = load_data("moon")
X, y = torch.cat([x_train]), torch.cat([y_train])
X_test, y_test = torch.cat([x_test]), torch.cat([y_test])

grease = GrEASE(n_components=2, spectral_hiddens=[128, 256], spectral_batch_size=1024,
                spectral_n_nbg=10)

X_new = grease.fit_transform(X)
X_test_new = grease.transform(X_test)

grassmann_distance = grease.grassmann_distance(X)
print(f"Grassmann distance: {grassmann_distance}")

grassmann_distance = grease.grassmann_distance(X, True)
print(f"Grassmann distance: {grassmann_distance}")

# visualize the embeddings
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].scatter(X_new[:, 0], X_new[:, 1], c=y, cmap='viridis', s=1)
axs[0].set_title("Train")
axs[1].scatter(X_test_new[:, 0], X_test_new[:, 1], c=y_test, cmap='viridis', s=1)
axs[1].set_title("Test")
plt.savefig("moon.png")
plt.show()
