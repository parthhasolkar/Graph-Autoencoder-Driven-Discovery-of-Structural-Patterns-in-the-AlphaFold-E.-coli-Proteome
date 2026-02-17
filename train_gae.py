import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os

EMBED_DIM = 64
HIDDEN_DIM = 96
EPOCHS = 10
LR = 0.001

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class GAE(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(HIDDEN_DIM, EMBED_DIM)
        )

    def forward(self, x):
        z = self.encoder(x)
        recon = z @ z.t()
        return recon, z

def main():
    files = os.listdir("../outputs/embeddings")
    sample = np.load(os.path.join("../outputs/embeddings", files[0]))
    input_dim = sample.shape[0]

    model = GAE(input_dim).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    for epoch in range(EPOCHS):
        optimizer.zero_grad()
        x = torch.tensor(sample, dtype=torch.float32).to(device)
        recon, z = model(x)
        loss = F.mse_loss(recon, recon.detach())
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss {loss.item():.4f}")

    np.save("../outputs/embeddings/protein_embeddings.npy", z.detach().cpu().numpy())

if __name__ == "__main__":
    main()
