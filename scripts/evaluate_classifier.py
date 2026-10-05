#!/usr/bin/env python3
"""Classical machine learning evaluation harness for stylometric authorship classification."""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from rightforge.ml.vectorizer import FEATURE_NAMES, StylometricVectorizer

# Sample synthetic corpus across three distinct writing styles
CORPUS_AUTHOR_A = [
    "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves.",
    "Mathematical calculations require rigorous discipline and uncompromising adherence to symbolic truth.",
    "A formal demonstration proceeds from indisputable axioms to necessarily valid conclusions through logic.",
    "We observe that deduction is the primary vehicle for navigating complex quantitative domains.",
    "Geometry and arithmetic establish the fundamental pillars upon which computational science rests.",
    "Every logical proposition must withstand rigorous scrutiny before inclusion in an academic proof.",
]

CORPUS_AUTHOR_B = [
    "The rain drummed against the windowpane, cold and relentless, washing away the city's neon reflections.",
    "He pulled his collar high against the biting wind, wondering if anyone was still following him through the dark.",
    "A lone streetlight flickered twice before dying, leaving the narrow alley steeped in suffocating blackness.",
    "Footsteps echoed across the wet cobblestones, quickening in pace as the fog rolled in from the harbor.",
    "She checked her wristwatch; midnight had come and gone, yet the courier had left no sign behind.",
    "Somewhere in the distance, a foghorn groaned, heavy with the weight of unseen ships lost in the tide.",
]

CORPUS_AUTHOR_C = [
    "Hey folks! Welcome back to another quick update, and boy do we have some exciting news today!",
    "Don't forget to hit like and subscribe if you're enjoying the content, it really helps the channel out!",
    "So here's the thing: we tried the new build and honestly, it completely blew our minds!",
    "Drop a comment down below and let us know what you think of this crazy new feature!",
    "We're going to wrap this up quickly, but make sure to check out the links in the description!",
    "Thanks for tuning in, you guys are absolutely amazing, and we'll catch you in the next one!",
]


def run_experiment() -> None:
    print("=================================================================")
    print(" RightForge: Classical ML Stylometric Authorship Benchmark")
    print("=================================================================")

    vectorizer = StylometricVectorizer()

    documents = CORPUS_AUTHOR_A + CORPUS_AUTHOR_B + CORPUS_AUTHOR_C
    labels = (
        ["Academic/Formal"] * len(CORPUS_AUTHOR_A)
        + ["Noir/Narrative"] * len(CORPUS_AUTHOR_B)
        + ["Casual/Blogger"] * len(CORPUS_AUTHOR_C)
    )

    print(f"Total documents: {len(documents)} ({len(CORPUS_AUTHOR_A)} per class)")
    print(f"Extracted feature count: {len(FEATURE_NAMES)}")

    # Vectorize documents
    X = vectorizer.transform(documents)
    y = np.array(labels)

    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    # 1. Scaled Logistic Regression evaluation
    lr_pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    lr_scores = cross_val_score(lr_pipe, X, y, cv=cv)

    print(f"\n[1] Logistic Regression (Scaled) 3-Fold CV Accuracy: {lr_scores.mean():.2%} (+/- {lr_scores.std():.2%})")

    # 2. Random Forest evaluation
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_scores = cross_val_score(rf, X, y, cv=cv)
    print(f"[2] Random Forest 3-Fold CV Accuracy:            {rf_scores.mean():.2%} (+/- {rf_scores.std():.2%})")

    # Fit RF to inspect top discriminative features
    rf.fit(X, y)
    importances = rf.feature_importances_
    ranked_indices = np.argsort(importances)[::-1]

    print("\nTop 8 Discriminative Stylometric Features:")
    print("-" * 55)
    for rank, idx in enumerate(ranked_indices[:8], 1):
        print(f" {rank}. {FEATURE_NAMES[idx]:<32} Importance: {importances[idx]:.4f}")
    print("-" * 55)

    # Full classification report on fit
    y_pred = rf.predict(X)
    print("\nTraining Set Diagnostic Classification Report:")
    print(classification_report(y, y_pred))


if __name__ == "__main__":
    run_experiment()
