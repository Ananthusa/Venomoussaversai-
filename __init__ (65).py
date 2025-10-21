import numpy as np
import scipy.signal as signal
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -----------------------
# 1) Generate synthetic EEG data
# -----------------------
def generate_eeg(n_samples=400, n_channels=8, fs=128):
    """Simulate EEG for LEFT (0) vs RIGHT (1) imagery"""
    n_points = int(1.0 * fs)  # 1 second epochs
    X = np.zeros((n_samples, n_channels, n_points))
    y = np.zeros(n_samples, dtype=int)
    t = np.arange(n_points) / fs

    for i in range(n_samples):
        cls = np.random.choice([0,1])
        y[i] = cls
        for ch in range(n_channels):
            noise = np.random.randn(n_points) * 0.5
            sig = noise
            if cls == 0 and ch < n_channels//2:
                sig += np.sin(2*np.pi*10*t)  # alpha (left imagery)
            if cls == 1 and ch >= n_channels//2:
                sig += np.sin(2*np.pi*20*t)  # beta (right imagery)
            X[i,ch] = sig
    return X, y, fs

# -----------------------
# 2) Extract bandpower features
# -----------------------
def bandpower(epoch, fs, band):
    f, Pxx = signal.welch(epoch, fs=fs, nperseg=128)
    idx = np.logical_and(f >= band[0], f <= band[1])
    return np.trapz(Pxx[idx], f[idx])

def extract_features(X, fs):
    bands = [(8,12), (12,30)]  # alpha & beta
    feats = []
    for epoch in X:
        epoch_feats = []
        for ch in epoch:
            for b in bands:
                epoch_feats.append(bandpower(ch, fs, b))
        feats.append(epoch_feats)
    return np.array(feats)

# -----------------------
# 3) Train/test
# -----------------------
X_raw, y, fs = generate_eeg()
X = extract_features(X_raw, fs)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

clf = LDA()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Educational 'mind read' accuracy:", accuracy_score(y_test, y_pred))