# spinex_timeseries.py


import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from scipy.spatial.distance import cdist
from scipy.stats import spearmanr
from functools import lru_cache
import hashlib
from sklearn.metrics import r2_score
from numba import jit
from multiprocessing import Pool
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize_scalar

@jit(nopython=True)
def numba_dtw(x, y):
    n, m = len(x), len(y)
    dtw_matrix = np.zeros((n+1, m+1))
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(x[i-1] - y[j-1])
            dtw_matrix[i, j] = cost + min(dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1])
    return dtw_matrix[n, m]

@jit(nopython=True)
def numba_dtw_similarity(X):
    n = X.shape[0]
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            dist = numba_dtw(X[i], X[j])
            sim_matrix[i, j] = sim_matrix[j, i] = 1 / (1 + dist)
    return sim_matrix

@jit(nopython=True)
def numba_sample_entropy(x, m=2, r=0.2):
    n = len(x)
    B = 0.0
    A = 0.0
    for i in range(n - m):
        for j in range(i + 1, n - m):
            matches = 0
            for k in range(m):
                if abs(x[i+k] - x[j+k]) <= r:
                    matches += 1
                else:
                    break
            if matches == m:
                B += 1
                if abs(x[i+m] - x[j+m]) <= r:
                    A += 1
    return -np.log((A + 1e-10) / (B + 1e-10))

# Function to calculate direction accuracy
def direction_accuracy(segment1, segment2):
    direction1 = np.sign(np.diff(segment1))
    direction2 = np.sign(np.diff(segment2))
    return np.mean(direction1 == direction2)

class SPINEX_Timeseries:
    def __init__(self, data, window_size=None, forecast_horizon=1, similarity_methods=None,
                dynamic_window=True, multi_level=True, dynamic_threshold=True):
        self.data = np.array(data)
        if window_size is None:
            self.window_size = max(10, len(data) // 10)
        else:
            self.window_size = min(window_size, len(data) // 2)
        self.forecast_horizon = min(forecast_horizon, len(data) // 10)
        self.forecast_horizon = forecast_horizon
        self.similarity_methods = similarity_methods if similarity_methods else ['direction', 'cosine', 'euclidean', 'dtw']
        self.similarity_cache = {}
        self.dynamic_window = dynamic_window
        self.multi_level = multi_level
        self.dynamic_threshold = dynamic_threshold
        self.segments_cache = {}
        self.recent_errors = []
        self.recent_similarity_scores = []
        if self.dynamic_window:
            self.window_size = self.adaptive_window_size()

    @staticmethod
    def hash_array(arr):
        return hashlib.md5(arr.data.tobytes()).hexdigest()

    @staticmethod
    def direction_similarity(X):
        n = X.shape[0]
        direction_matrix = np.sign(np.diff(X, axis=1))
        sim_matrix = np.dot(direction_matrix, direction_matrix.T)
        sim_matrix = sim_matrix / (direction_matrix.shape[1])  # Normalize by the length of the direction vectors
        return sim_matrix

    @lru_cache(maxsize=128)
    def get_similarity_matrix(self, method, segments_hash):
        if (segments_hash, method) in self.similarity_cache:
            return self.similarity_cache[(segments_hash, method)]
        segments = self.segments_cache[segments_hash]
        if method == 'cosine':
            similarity_matrix = self.cosine_similarity(segments)
        elif method == 'correlation':
            similarity_matrix = self.correlation_similarity(segments)
        elif method == 'euclidean':
            similarity_matrix = self.euclidean_similarity(segments)
        elif method == 'spearman':
            similarity_matrix = self.spearman_similarity(segments)
        elif method == 'dtw':
            similarity_matrix = numba_dtw_similarity(segments)
        elif method == 'direction':
            similarity_matrix = self.direction_similarity(segments)
        else:
            raise ValueError(f"Invalid similarity method: {method}")
        self.similarity_cache[(segments_hash, method)] = similarity_matrix
        return similarity_matrix

    @staticmethod
    def cosine_similarity(X):
        norm = np.linalg.norm(X, axis=1)
        return np.dot(X, X.T) / np.outer(norm, norm)

    @staticmethod
    def correlation_similarity(X):
        return np.corrcoef(X)

    @staticmethod
    def euclidean_similarity(X):
        sq_dists = cdist(X, X, metric='euclidean')**2
        return 1 / (1 + np.sqrt(sq_dists))

    @staticmethod
    def spearman_similarity(X):
        return spearmanr(X.T)[0]

    def adjust_dynamic_parameters(self):
        # Constants for scaling
        MIN_WINDOW_SIZE = 10
        MAX_WINDOW_SIZE = len(self.data) // 2
        BASELINE_WINDOW_SIZE = max(MIN_WINDOW_SIZE, len(self.data) // 10)
        # Calculate recent volatility using rolling window
        if len(self.data) > BASELINE_WINDOW_SIZE:
            volatility = np.std(self.data[-BASELINE_WINDOW_SIZE:])
        else:
            volatility = np.std(self.data)
        # Adjust window size inversely with volatility
        scale_factor = np.clip(volatility, 0.1, 1.0)  # Limiting scale factor to avoid extreme values
        self.window_size = int(MAX_WINDOW_SIZE / scale_factor)
        self.window_size = max(MIN_WINDOW_SIZE, min(self.window_size, MAX_WINDOW_SIZE))
        # Adjust similarity threshold based on recent prediction performance if available
        if hasattr(self, 'recent_errors'):
            recent_error_mean = np.mean(self.recent_errors)
            recent_error_std = np.std(self.recent_errors)
            threshold_adjustment = recent_error_mean + recent_error_std
        else:
            threshold_adjustment = 0
        # Adjust the threshold based on mean and standard deviation of recent similarity scores
        if hasattr(self, 'recent_similarity_scores') and self.recent_similarity_scores:
            mean_sim = np.mean(self.recent_similarity_scores)
            std_sim = np.std(self.recent_similarity_scores)
            self.threshold = mean_sim + std_sim + threshold_adjustment
        else:
            self.threshold = 0.5  # Default threshold if no recent similarities are recorded
        print(f"Adjusted Window Size: {self.window_size}, Threshold: {self.threshold}")

    def get_dynamic_threshold(self, similarities):
        if self.dynamic_threshold:
            mean_sim = np.mean(similarities)
            std_sim = np.std(similarities)
            base_threshold = mean_sim + std_sim  # Basic dynamic threshold
            # Adjust threshold based on the number of similarities above it
            if len(similarities[similarities > base_threshold]) < 5:
                # If less than 5 indices are above threshold, reduce it to include more indices
                adjusted_threshold = np.percentile(similarities, 90)  # Adjusting percentile upward
            else:
                adjusted_threshold = base_threshold
            print(f"Dynamic Threshold Adjusted: {adjusted_threshold}")
            return adjusted_threshold
        else:
            # Fallback to a fixed percentile if dynamic thresholding is turned off
            return np.percentile(similarities, 95)

    def adjusted_dtw_similarity(self, X):
        # Adjust the DTW calculation to be more forgiving
        dtw_scores = numba_dtw_similarity(X)
        adjusted_scores = 1 / (1 + np.sqrt(dtw_scores))  # Squaring DTW scores for more lenience
        return adjusted_scores

    def plot_prediction(self):
        predicted_values = self.predict()
        if predicted_values.size > 0:
            prediction_start_index = len(self.data) - self.forecast_horizon
            plt.figure(figsize=(12, 6))
            plt.plot(self.data, label='Actual Time Series', color='blue')
            plt.plot(np.arange(prediction_start_index, len(self.data)),
                     self.data[prediction_start_index:], label='Actual (Prediction Window)', color='green')
            plt.plot(np.arange(prediction_start_index, len(self.data)),
                     predicted_values, label='Predicted', color='red', linestyle='--')
            plt.title('Time Series Prediction Comparison')
            plt.xlabel('Time Index')
            plt.ylabel('Values')
            plt.legend()
            plt.show()
        else:
            print("No valid predictions could be made.")

    @lru_cache(maxsize=32)
    def extract_segments(self, window_size=None):
        if window_size is None:
            window_size = self.adaptive_window_size()
        data_length = len(self.data)
        if data_length < window_size:
            print(f"Data length ({data_length}) is less than window size ({window_size}). Adjusting window size.")
            window_size = data_length // 2  # Use half of data length as window size
        n = data_length - window_size + 1
        if n <= 1:
            return np.array([self.data[-window_size:]])
        segments = np.lib.stride_tricks.sliding_window_view(self.data, window_size)
        # Normalize segments to handle different scales
        segment_means = np.mean(segments, axis=1)
        segment_stds = np.std(segments, axis=1)
        normalized_segments = (segments - segment_means[:, np.newaxis]) / (segment_stds[:, np.newaxis] + 1e-8)
        return normalized_segments

    def find_similar_segments(self):
        window_sizes = [self.window_size]
        if self.multi_level:
            window_sizes = [max(2, self.window_size // 2)] + window_sizes + [min(len(self.data) // 4, self.window_size * 2)]
        all_similarities = []
        for w_size in window_sizes:
            segments = self.extract_segments(w_size)
            if len(segments) < 2:
                print(f"Not enough segments for window size {w_size}, skipping.")
                continue
            segments_hash = self.hash_array(segments)
            self.segments_cache[segments_hash] = segments
            method_similarities = []
            for method in self.similarity_methods:
                if method == 'dtw' and len(segments) > 500:
                    print(f"DTW skipped for large dataset with {len(segments)} segments.")
                    continue
                try:
                    sim_matrix = self.get_similarity_matrix(method, segments_hash)
                    if sim_matrix.ndim > 1:
                        method_similarities.append(sim_matrix[-1, :-1])
                    else:
                        method_similarities.append(sim_matrix[:-1])
                except Exception as e:
                    print(f"Error calculating similarity for method {method}: {str(e)}")
            if not method_similarities:
                print(f"No valid similarity methods for window size {w_size}, skipping.")
                continue
            min_length = min(len(sim) for sim in method_similarities)
            method_similarities = [sim[-min_length:] for sim in method_similarities]
            method_similarities_array = np.array(method_similarities)
            overall_similarity = np.nanmean(method_similarities_array, axis=0)
            all_similarities.append(overall_similarity)
        if not all_similarities:
            print("No similarities found for any window size. Using fallback similarity.")
            return self.fallback_similarity_method()
        min_length = min(len(s) for s in all_similarities)
        all_similarities = [s[-min_length:] for s in all_similarities]
        all_similarities_array = np.array(all_similarities)
        combined_similarities = np.nanmean(all_similarities_array, axis=0)
        return combined_similarities

    def fallback_similarity_method(self):
        # Simple autocorrelation-based similarity
        acf = np.correlate(self.data, self.data, mode='full')[len(self.data)-1:]
        return acf / acf[0]  # Normalize

    def analyze_segment_similarity(self, segment_index):
        current_segment = self.extract_segments(self.window_size)[-1]
        historical_segment = self.extract_segments(self.window_size)[segment_index]
        similarity_scores = {}
        for method in self.similarity_methods:
            if method == 'cosine':
                score = np.dot(current_segment, historical_segment) / (np.linalg.norm(current_segment) * np.linalg.norm(historical_segment))
            elif method == 'euclidean':
                score = 1 / (1 + np.linalg.norm(current_segment - historical_segment))
            elif method == 'dtw':
                score = 1 / (1 + numba_dtw(current_segment, historical_segment))
            elif method == 'correlation':
                score, _ = np.corrcoef(current_segment, historical_segment)[0, 1]
            elif method == 'spearman':
                score, _ = spearmanr(current_segment, historical_segment)
            elif method == 'direction':
                score = direction_accuracy(current_segment, historical_segment)
            else:
                raise ValueError(f"Invalid similarity method: {method}")
            similarity_scores[method] = score
        feature_contributions = np.abs(current_segment - historical_segment)
        top_contributing_features = np.argsort(feature_contributions)[::-1][:5]
        return {
            'similarity_scores': similarity_scores,
            'top_contributing_features': top_contributing_features.tolist(),
            'feature_contributions': feature_contributions.tolist()
        }

    def get_nearest_neighbors(self, k=5):
        similarities = self.find_similar_segments()
        nearest_indices = np.argsort(similarities)[::-1][:k]
        return [(idx, similarities[idx]) for idx in nearest_indices]

    def dtw_similarity(self, X):
        return numba_dtw_similarity(X)  # Use the global function

    def adaptive_window_size(self):
        data_length = len(self.data)
        # Even more conservative window sizing
        if data_length < 100:
            base_window = max(2, data_length // 20)
        elif data_length < 1000:
            base_window = max(5, data_length // 40)
        else:
            base_window = max(25, data_length // 80)
        # Detect potential seasonality
        potential_seasons = self.detect_seasonality()
        # Calculate data variability
        variability = np.std(self.data) / (np.mean(self.data) + 1e-8)
        # Adjust window based on seasonality and variability
        if potential_seasons:
            window = min(max(potential_seasons), base_window)
        else:
            window = int(base_window * (1 + variability))
        return max(2, min(window, data_length // 8))  # Ensure window is at most 1/8 of data length

    def detect_seasonality(self, max_lag=None):
        if max_lag is None:
            max_lag = len(self.data) // 2
        acf = np.correlate(self.data, self.data, mode='full')[-max_lag:]
        peaks = np.where((acf[1:-1] > acf[:-2]) & (acf[1:-1] > acf[2:]))[0] + 1
        if len(peaks) > 0:
            return [int(peaks[0])]  # Return a list with the first peak
        return []  # Return an empty list if no peaks found

    def detect_anomalies(self, threshold_percentile=2):
        segments = self.extract_segments(self.window_size)
        similarities = self.find_similar_segments()
        threshold = np.percentile(similarities, threshold_percentile)
        anomaly_indices = np.where(similarities < threshold)[0]
        anomalies = []
        for idx in anomaly_indices:
            start = idx
            end = idx + self.window_size
            anomalies.append({
                'start_index': start,
                'end_index': end,
                'segment': self.data[start:end].tolist(),
                'similarity_score': similarities[idx]
            })
        return anomalies, threshold

    def plot_anomalies(self, threshold_percentile=5):
        anomalies, threshold = self.detect_anomalies(threshold_percentile)
        plt.figure(figsize=(12, 6))
        plt.plot(self.data, label='Time Series', color='blue')
        for anomaly in anomalies:
            plt.axvspan(anomaly['start_index'], anomaly['end_index'], color='red', alpha=0.3)
        plt.title(f'Time Series with Detected Anomalies (Threshold: {threshold:.4f})')
        plt.xlabel('Time Index')
        plt.ylabel('Values')
        plt.legend()
        if not anomalies:
            plt.text(0.5, 0.5, 'No anomalies detected', horizontalalignment='center',
                    verticalalignment='center', transform=plt.gca().transAxes)
        else:
            print(f"Detected {len(anomalies)} anomalies")
        plt.show()
        similarities = self.find_similar_segments()
        print(f"Similarity score range: {similarities.min():.4f} to {similarities.max():.4f}")
        print(f"Similarity score mean: {similarities.mean():.4f}")
        print(f"Similarity score median: {np.median(similarities):.4f}")
        print(f"Anomaly threshold: {threshold:.4f}")

    def calculate_mean_squared_error(self, actual, predicted):
        return np.mean((actual - predicted) ** 2)

    def calculate_basic_similarity(self, actual, predicted):
        # Ensuring that neither actual nor predicted are empty to avoid runtime errors
        if actual.size == 0 or predicted.size == 0:
            return np.nan
        correlation = np.corrcoef(actual, predicted)[0, 1]
        return correlation

    def fallback_prediction(self, num_points):
        if len(self.data) < num_points * 2:
            raise ValueError("Insufficient data for prediction")

        # Adaptive window sizing for trend extraction
        def adaptive_window(data):
            def mse(window):
                trend = extract_trend(data, int(window))
                return np.mean((data[int(window)-1:] - trend)**2)
            result = minimize_scalar(mse, bounds=(10, len(data)//2), method='bounded')
            return int(result.x)

        def extract_trend(data, window_size):
            return np.convolve(data, np.ones(window_size), 'valid') / window_size

        # Multiple seasonality detection
        def detect_seasonalities(data, max_period, num_seasons=2):
            correlations = [np.corrcoef(data[:-i], data[i:])[0, 1] for i in range(1, max_period)]
            seasons = []
            for _ in range(num_seasons):
                if len(correlations) > 0:
                    season = np.argmax(correlations) + 1
                    seasons.append(season)
                    correlations[season-1] = -1  # Remove detected season
            return seasons

        # Non-linear trend modeling
        def model_nonlinear_trend(data, x):
            coeffs = np.polyfit(x, data, 3)
            return np.poly1d(coeffs)

        # Anomaly detection
        def detect_anomalies(data, threshold=3):
            mean = np.mean(data)
            std = np.std(data)
            return np.abs(data - mean) > threshold * std

        # Decompose the time series
        window_size = adaptive_window(self.data)
        trend = extract_trend(self.data, window_size)
        detrended = self.data[window_size-1:] - trend
        seasonality_periods = detect_seasonalities(detrended, num_points)

        # Extract seasonal components
        seasonals = []
        for period in seasonality_periods:
            seasonal = np.zeros(period)
            for i in range(period):
                seasonal[i] = np.mean(detrended[i::period])
            seasonals.append(seasonal)

        # Calculate residuals
        combined_seasonal = np.zeros_like(detrended)
        for seasonal in seasonals:
            combined_seasonal += np.tile(seasonal, len(detrended) // len(seasonal) + 1)[:len(detrended)]
        residuals = detrended - combined_seasonal[:len(detrended)]

        # Detect and handle anomalies
        anomalies = detect_anomalies(residuals)
        cleaned_residuals = residuals.copy()
        cleaned_residuals[anomalies] = np.median(residuals)

        # Predict trend (non-linear)
        x = np.arange(len(self.data))
        trend_model = model_nonlinear_trend(self.data, x)
        future_x = np.arange(len(self.data), len(self.data) + self.forecast_horizon)
        future_trend = trend_model(future_x)

        # Predict seasonal components
        future_seasonal = np.zeros(self.forecast_horizon)
        for seasonal in seasonals:
            future_seasonal += np.tile(seasonal, self.forecast_horizon // len(seasonal) + 1)[:self.forecast_horizon]

        # Predict residuals using a custom method with confidence intervals
        def predict_residuals_with_ci(residuals, horizon, confidence=0.95):
            weights = np.exp(np.linspace(-1, 0, len(residuals)))
            weighted_mean = np.sum(residuals * weights) / np.sum(weights)
            weighted_std = np.sqrt(np.sum(weights * (residuals - weighted_mean)**2) / np.sum(weights))
            predictions = np.random.normal(weighted_mean, weighted_std, (1000, horizon))
            mean_prediction = np.mean(predictions, axis=0)
            ci_lower = np.percentile(predictions, (1 - confidence) / 2 * 100, axis=0)
            ci_upper = np.percentile(predictions, (1 + confidence) / 2 * 100, axis=0)
            return mean_prediction, ci_lower, ci_upper

        future_residuals, ci_lower, ci_upper = predict_residuals_with_ci(cleaned_residuals, self.forecast_horizon)

        # Combine predictions
        predictions = future_trend + future_seasonal + future_residuals
        ci_lower += future_trend + future_seasonal
        ci_upper += future_trend + future_seasonal

        return predictions, ci_lower, ci_upper

    # Automated hyperparameter tuning
    def tune_hyperparameters(self):
        # Example: tune the number of seasonalities to detect
        best_num_seasons = 1
        best_mse = float('inf')
        for num_seasons in range(1, 5):
            predictions, _, _ = self.fallback_prediction(num_points=20)
            mse = np.mean((self.data[-len(predictions):] - predictions)**2)
            if mse < best_mse:
                best_mse = mse
                best_num_seasons = num_seasons
        return {'num_seasons': best_num_seasons}

    def predict(self):
        self.adjust_dynamic_parameters()
        try:
            similarities = self.find_similar_segments()
            if len(similarities) == 0:
                print("No similarities found. Using fallback prediction.")
                return self.fallback_prediction(self.forecast_horizon)[0]
            threshold = self.get_dynamic_threshold(similarities)
            valid_indices = []
            # Adaptive thresholding
            for percentile in range(95, 70, -5):  # Start at 95th percentile, go down to 70th
                top_indices = np.where(similarities > np.percentile(similarities, percentile))[0]
                valid_indices = top_indices[top_indices + self.window_size + self.forecast_horizon <= len(self.data)]
                if len(valid_indices) >= 3:
                    break
            if len(valid_indices) == 0:
                print("No valid indices found. Using fallback prediction.")
                return self.fallback_prediction(self.forecast_horizon)[0]
            predictions = []
            weights = []
            for idx in valid_indices:
                start = idx + self.window_size
                end = start + self.forecast_horizon
                if end <= len(self.data):
                    segment = self.data[start:end]
                    predictions.append(segment)
                    weights.append(similarities[idx])
            if predictions:
                min_length = min(len(p) for p in predictions)
                predictions = [p[:min_length] for p in predictions]
                predictions = np.array(predictions)
                weights = np.array(weights)
                # Adjust predictions to align with the most recent data point
                last_actual = self.data[-1]
                for i in range(len(predictions)):
                    shift = last_actual - predictions[i][0]
                    predictions[i] += shift
                predicted_values = np.average(predictions, axis=0, weights=weights)
            else:
                print("No valid predictions. Using fallback prediction.")
                predicted_values = self.fallback_prediction(self.forecast_horizon)[0]
        except Exception as e:
            print(f"Error in predict: {str(e)}")
            predicted_values = self.fallback_prediction(self.forecast_horizon)[0]  # Return only predictions, not CI
        if predicted_values.size > 0:
            actual_values = self.data[-len(predicted_values):]
            prediction_error = self.calculate_mean_squared_error(actual_values, predicted_values)
            recent_similarity_score = self.calculate_basic_similarity(actual_values, predicted_values)
            self.update_recent_performance(prediction_error, recent_similarity_score)
        else:
            self.update_recent_performance(np.nan, np.nan)
        return predicted_values

    def update_recent_performance(self, new_error, new_similarity_score):
        self.recent_errors.append(new_error)
        self.recent_similarity_scores.append(new_similarity_score)
        # Optionally, trim these lists to avoid unlimited growth
        self.recent_errors = self.recent_errors[-100:]  # Keep the last 100 records
        self.recent_similarity_scores = self.recent_similarity_scores[-100:]

    def evaluate_prediction(self, actual, predicted):
        if len(actual) != len(predicted):
            raise ValueError("Actual and predicted arrays must have the same length.")
        if len(actual) == 0:
            return {metric: np.nan for metric in ['MSE', 'MAE', 'RMSE', 'MAPE', 'SMAPE', 'R-squared', 'Direction Accuracy', 'Theil\'s U']}
        mse = np.mean((actual - predicted) ** 2)
        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((actual - predicted) / (actual + 1e-8))) * 100
        smape = np.mean(2 * np.abs(predicted - actual) / (np.abs(actual) + np.abs(predicted) + 1e-8)) * 100
        r2 = r2_score(actual, predicted)
        direction_actual = np.sign(np.diff(actual))
        direction_pred = np.sign(np.diff(predicted))
        direction_accuracy = np.mean(direction_actual == direction_pred) * 100
        actual_changes = np.diff(actual)
        predicted_changes = np.diff(predicted)
        theil_u = np.sqrt(np.sum(predicted_changes**2) / np.sum(actual_changes**2)) if np.sum(actual_changes**2) != 0 else np.nan
        return {
            'MSE': mse, 'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'SMAPE': smape,
            'R-squared': r2, 'Direction Accuracy': direction_accuracy, 'Theil\'s U': theil_u
        }

    def validate_prediction(self, splits=3):
            n_samples = len(self.data)
            max_splits = (n_samples - self.window_size) // self.forecast_horizon
            splits = min(splits, max_splits)
            if splits < 2:
                print("Warning: Not enough data for multiple splits. Performing single train-test split.")
                train_size = int(0.8 * n_samples)
                train, test = self.data[:train_size], self.data[train_size:]
                self.data = train
                self.similarity_cache = {}
                predicted = self.predict()
                if predicted.size > 0:
                    actual = test[:len(predicted)]
                    metrics = self.evaluate_prediction(actual, predicted)
                    self.data = np.concatenate((train, test))  # Restore original data
                    return metrics
                else:
                    print("Insufficient data to make a prediction.")
                    return None
            tscv = TimeSeriesSplit(n_splits=splits, test_size=self.forecast_horizon)
            errors = []
            for train_index, test_index in tscv.split(self.data):
                if len(train_index) < self.window_size:
                    print(f"Warning: Train set too small for window size. Skipping split.")
                    continue
                train, test = self.data[train_index], self.data[test_index]
                original_data = self.data
                self.data = train
                self.similarity_cache = {}
                predicted = self.predict()
                if predicted.size > 0:
                    actual = test[:len(predicted)]
                    metrics = self.evaluate_prediction(actual, predicted)
                    errors.append(metrics)
                else:
                    print("Insufficient data to predict for this split.")
                self.data = original_data
            if errors:
                avg_metrics = {metric: np.mean([e[metric] for e in errors if metric in e]) for metric in errors[0]}
                return avg_metrics
            else:
                print("No valid predictions could be made across splits.")
                return None

    def get_explainability_results(self, top_k=5):
        similarities = self.find_similar_segments()
        threshold = self.get_dynamic_threshold(similarities)
        top_indices = np.where(similarities > threshold)[0]
        if len(top_indices) == 0:
            top_indices = np.argsort(similarities)[-top_k:]
        results = {
            'top_similar_segments': top_indices.tolist(),
            'similarity_scores': similarities[top_indices].tolist(),
            'threshold': threshold,
            'segment_contributions': []
        }
        predictions = []
        valid_indices = []
        for idx in top_indices:
            start = idx + self.window_size
            if start + self.forecast_horizon <= len(self.data):
                predictions.append(self.data[start:start + self.forecast_horizon])
                valid_indices.append(idx)
        if not predictions:
            return results
        predictions = np.array(predictions)
        weights = similarities[valid_indices]
        weighted_predictions = predictions * weights[:, np.newaxis]
        for i, (index, score, prediction, contribution) in enumerate(zip(valid_indices, similarities[valid_indices], predictions, weighted_predictions)):
            results['segment_contributions'].append({
                'segment_index': int(index),
                'similarity_score': float(score),
                'prediction': prediction.tolist(),
                'weighted_contribution': contribution.tolist(),
                'contribution_percentage': (contribution / np.sum(weighted_predictions, axis=0) * 100).tolist()
            })
        return results

    def plot_nearest_neighbors(self, k=5):
        current_segment = self.extract_segments(self.window_size)[-1]
        neighbors = self.get_nearest_neighbors(k)
        plt.figure(figsize=(15, 10))
        plt.subplot(k+1, 1, 1)
        plt.plot(current_segment, color='blue', label='Current Segment')
        plt.title('Current Segment')
        plt.legend()
        for i, (idx, similarity) in enumerate(neighbors, start=2):
            neighbor_segment = self.extract_segments(self.window_size)[idx]
            plt.subplot(k+1, 1, i)
            plt.plot(neighbor_segment, color='red', label=f'Neighbor {i-1}')
            plt.title(f'Neighbor {i-1} (Similarity: {similarity:.4f})')
            plt.legend()
        plt.tight_layout()
        plt.show()

    def analyze_and_plot_neighbors(self, k=5):
        current_segment = self.extract_segments(self.window_size)[-1]
        neighbors = self.get_nearest_neighbors(k)
        plt.figure(figsize=(20, 5*k))
        plt.subplot(k+1, 2, 1)
        plt.plot(current_segment, color='blue', label='Current Segment')
        plt.title('Current Segment')
        plt.legend()
        for i, (idx, overall_similarity) in enumerate(neighbors, start=1):
            neighbor_segment = self.extract_segments(self.window_size)[idx]
            analysis = self.analyze_segment_similarity(idx)
            plt.subplot(k+1, 2, 2*i+1)
            plt.plot(neighbor_segment, color='red', label=f'Neighbor {i}')
            plt.title(f'Neighbor {i} (Overall Similarity: {overall_similarity:.4f})')
            plt.legend()
            plt.subplot(k+1, 2, 2*i+2)
            methods = list(analysis['similarity_scores'].keys())
            scores = list(analysis['similarity_scores'].values())
            plt.bar(methods, scores)
            plt.title(f'Similarity Scores for Neighbor {i}')
            plt.ylim(0, 1)
            print(f"\nNeighbor {i} Analysis:")
            print(f"Overall Similarity: {overall_similarity:.4f}")
            print("Similarity Scores:")
            for method, score in analysis['similarity_scores'].items():
                print(f"  {method}: {score:.4f}")
            print("Top Contributing Features:", analysis['top_contributing_features'])
        plt.tight_layout()
        plt.show()
