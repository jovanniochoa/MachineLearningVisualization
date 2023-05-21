import pickle

# Assuming you have a trained model
model = ...  # Your trained model

# Save the model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
