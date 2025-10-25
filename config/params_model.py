from scipy.stats import uniform, randint

lightgbm_hyperparameters = {
    'num_leaves': randint(20, 150),
    'learning_rate': uniform(0.01, 0.3),
    'n_estimators': randint(50, 500),
    'max_depth': randint(3, 15),
    'boosting_type': ['gbdt', 'dart', 'goss'],
}


random_search_for_the_best_hyperparameters = {
    'n_iter': 2,
    'cv': 2,
    'verbose': 2,
    'n_jobs': -1,
    'random_state': 42,
    'scoring': 'accuracy'
}