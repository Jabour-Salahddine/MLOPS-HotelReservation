import pandas as pd
from scipy.stats import randint
import joblib
import config.paths as paths
import config.params_model as params
from src.applogger import get_logger
from src.specialExceptionHandling import CustException
from utils.fonctions_common import read_yaml, load_data
import os

import lightgbm as lgb
from sklearn.metrics import accuracy_score,precision_score,recall_score, f1_score,classification_report
from sklearn.model_selection import RandomizedSearchCV
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class Training:
    def __init__(self,train_path, test_path,model_path):
        self.train_path = train_path
        self.test_path = test_path
        self.medel_path = model_path
        self.hyperparams = params.lightgbm_hyperparameters
        self.random_search_params = params.random_search_for_the_best_hyperparameters


    def data_load(self):
        try:
            logger.info("Strating data loading from path : {}".format(self.train_path))
            train_df = load_data(self.train_path)

            logger.info(f"Strating data loading from path : {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error in data loading: {e}")
            raise CustException("Failed in data loading", e)
    
    def model_training(self,X_train,y_train):
        try:
            logger.info("Starting model training")
            lgbm = lgb.LGBMClassifier(random_state=42)
            random_search = RandomizedSearchCV(
                estimator=lgbm,
                param_distributions=self.hyperparams,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                verbose=self.random_search_params['verbose'],
                n_jobs=self.random_search_params['n_jobs'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )

            logger.info("Fitting the model with RandomizedSearchCV :")
            random_search.fit(X_train, y_train)

            logger.info(f"Best hyperparameters found: {random_search.best_params_}")
            best_model = random_search.best_estimator_
            return best_model
        except Exception as e:
            logger.error(f"error in model training:{e}")
    
            raise CustException("Failed in model training", e)

    def model_evaluation(self,model,X_test,y_test):
        try:
            logger.info("Starting model evaluation")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            logger.info(f"Model Evaluation Metrics:\n Accuracy: {accuracy}\n Precision: {precision}\n Recall: {recall}\n F1-Score: {f1}")
            logger.info(f"Classification Report:\n {classification_report(y_test, y_pred)}")

            return { 'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1_score': f1 }
        except Exception as e:
            logger.error(f"error in model evaluation:{e}")
            raise CustException("Failed in model evaluation", e)

    def save_model(self,model):
        try:
            logger.info("Starting model saving process")
            os.makedirs(os.path.dirname(self.medel_path), exist_ok=True)
            joblib.dump(model, self.medel_path)
            logger.info(f"Model saved successfully at {self.medel_path}")
        except Exception as e:
            logger.error(f"error in model saving:{e}")
            raise CustException("Failed in model saving", e)


    def run_training_pipeline(self):
        try:
            with mlflow.start_run():
                logger.info("Running the training pipeline : Mlflow run started")
                logger.info("Loading data with de fucntion data_load() :")
                X_train, y_train, X_test, y_test = self.data_load()
                
                logger.info("upload data as artifact in mlflow :")
                mlflow.log_artifact(self.train_path, artifact_path="data/train")
                mlflow.log_artifact(self.test_path, artifact_path="data/test")
                logger.info("Data uploaded successfully")

                logger.info("Training model with the function model_training() :")
                model = self.model_training(X_train, y_train)
                logger.info("Model trained successfully")

                logger.info("Evaluating model with the function model_evaluation() :")
                metrics = self.model_evaluation(model, X_test, y_test)
                logger.info("Model evaluated successfully")

                logger.info("saving model with the function save_model() :")
                self.save_model(model)
                logger.info("Model saved successfully")

                logger.info("logging model into mlflow :")
                mlflow.log_artifact(self.medel_path, artifact_path="model")
                logger.info("Model logged successfully")

                logger.info("Logging metrics into mlflow :")
                mlflow.log_metrics(metrics)
                logger.info("Metrics logged successfully")

                logger.info("loggig parameters into mlflow :")
                mlflow.log_params(model.get_params())
                logger.info("Parameters logged successfully")

                logger.info("Training pipeline completed successfully")
        except Exception as e:
            logger.error(f"error in training pipeline:{e}")
            raise CustException("Failed in training pipeline", e)



if __name__ == "__main__":

    training = Training(train_path=paths.PROCESSED_TRAIN_FILE_PATH,
                        test_path=paths.PROCESSED_TEST_FILE_PATH,
                        model_path=paths.MODEL_TRAINED_PATH)  
    training.run_training_pipeline()  





