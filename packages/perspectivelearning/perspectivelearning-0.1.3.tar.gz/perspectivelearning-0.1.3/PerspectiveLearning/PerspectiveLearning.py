import numpy as np
import pandas as pd
import random
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score

def ensure_2d(array):
    if array.ndim == 1:
        return array.reshape(-1, 1)
    return array


def generate_synthetic_data_linear(n_samples=100, random_state=42, noise=5.0):
    rng = np.random.RandomState(random_state)
    TEMPERATURE = rng.randint(20, 40, size=n_samples)
    CAPACITY = rng.randint(450, 600, size=n_samples)
    SPEED = rng.randint(10, 20, size=n_samples)
    DOOR_OPENING_TIME = rng.randint(2, 6, size=n_samples)
    p = rng.rand(n_samples) * 5.0
    q = rng.randint(30, 50, size=n_samples)
    r = rng.rand(n_samples) * 5.0

    outcomes = (
        50
        + 0.3 * TEMPERATURE
        + 0.4 * CAPACITY
        + 2.0 * SPEED
        + 3.0 * p
        + 0.1 * q
        + 1.5 * r
    )
    outcomes += 150
    # Add noise
    outcomes += rng.randn(n_samples) * noise

    threshold = np.median(outcomes)
    binary_class = (outcomes > threshold).astype(int)

    df = pd.DataFrame({
        "TEMPERATURE": ensure_2d(TEMPERATURE).flatten(),
        "CAPACITY": ensure_2d(CAPACITY).flatten(),
        "SPEED": ensure_2d(SPEED).flatten(),
        "DOOR_OPENING_TIME": ensure_2d(DOOR_OPENING_TIME).flatten(),
        "p": ensure_2d(p).flatten(),
        "q": ensure_2d(q).flatten(),
        "r": ensure_2d(r).flatten(),
        "OUTCOMES": ensure_2d(outcomes).flatten(),
        "CLASS": ensure_2d(binary_class).flatten()
    })
    return df


def generate_synthetic_data_poly(n_samples=100, random_state=42, noise=5.0):
    rng = np.random.RandomState(random_state)
    TEMPERATURE = rng.randint(20, 40, size=n_samples)
    CAPACITY = rng.randint(450, 600, size=n_samples)
    SPEED = rng.randint(10, 20, size=n_samples)
    DOOR_OPENING_TIME = rng.randint(2, 6, size=n_samples)
    p = rng.rand(n_samples) * 5.0
    q = rng.randint(30, 50, size=n_samples)
    r = rng.rand(n_samples) * 5.0

    outcomes = 200.0 + 1e-3 * (CAPACITY ** 2) + (TEMPERATURE * SPEED) * 0.3 + (p ** 2) * 2.0 + (r ** 2) * 1.5
    # Add noise
    outcomes += rng.randn(n_samples) * noise

    threshold = np.median(outcomes)
    binary_class = (outcomes > threshold).astype(int)

    df = pd.DataFrame({
        "TEMPERATURE": ensure_2d(TEMPERATURE).flatten(),
        "CAPACITY": ensure_2d(CAPACITY).flatten(),
        "SPEED": ensure_2d(SPEED).flatten(),
        "DOOR_OPENING_TIME": ensure_2d(DOOR_OPENING_TIME).flatten(),
        "p": ensure_2d(p).flatten(),
        "q": ensure_2d(q).flatten(),
        "r": ensure_2d(r).flatten(),
        "OUTCOMES": ensure_2d(outcomes).flatten(),
        "CLASS": ensure_2d(binary_class).flatten()
    })
    return df


def generate_synthetic_data_sigmoid(n_samples=100, random_state=42, noise=5.0):
    rng = np.random.RandomState(random_state)
    TEMPERATURE = rng.randint(20, 40, size=n_samples)
    CAPACITY = rng.randint(450, 600, size=n_samples)
    SPEED = rng.randint(10, 20, size=n_samples)
    DOOR_OPENING_TIME = rng.randint(2, 6, size=n_samples)
    p = rng.rand(n_samples) * 5.0
    q = rng.randint(30, 50, size=n_samples)
    r = rng.rand(n_samples) * 5.0

    logit = 0.01 * CAPACITY + 0.2 * TEMPERATURE + p + 0.5 * r - 5.0
    sigmoid = 1.0 / (1.0 + np.exp(-logit))
    outcomes = 200 + sigmoid * 15.0
    # Add noise
    outcomes += rng.randn(n_samples) * noise

    threshold = np.median(outcomes)
    binary_class = (outcomes > threshold).astype(int)

    df = pd.DataFrame({
        "TEMPERATURE": ensure_2d(TEMPERATURE).flatten(),
        "CAPACITY": ensure_2d(CAPACITY).flatten(),
        "SPEED": ensure_2d(SPEED).flatten(),
        "DOOR_OPENING_TIME": ensure_2d(DOOR_OPENING_TIME).flatten(),
        "p": ensure_2d(p).flatten(),
        "q": ensure_2d(q).flatten(),
        "r": ensure_2d(r).flatten(),
        "OUTCOMES": ensure_2d(outcomes).flatten(),
        "CLASS": ensure_2d(binary_class).flatten()
    })
    return df

class PerspectiveLearning:
    def __init__(
        self,
        dataset: pd.DataFrame,
        features: list,
        target: str,
        learning_rate: float = 0.01,
        epochs: int = 100,
        batch_size: int = 16,
        optimizer: str = "adamw",
        lambda_reg: float = 0.001,
        n_splits: int = 5,
        patience: int = 10,
        gradient_clip_value: float = 1.0,
        max_auto_perspectives: int = 5,
        do_polynomial_expansion: bool = True,
        poly_degree: int = 2,
        random_state: int = 42
    ):
        self.dataset = dataset.copy()
        self.features = features
        self.target = target
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.optimizer = optimizer.lower()
        self.lambda_reg = lambda_reg
        self.n_splits = n_splits
        self.patience = patience
        self.gradient_clip_value = gradient_clip_value
        self.max_auto_perspectives = max_auto_perspectives
        self.do_polynomial_expansion = do_polynomial_expansion
        self.poly_degree = poly_degree
        self.random_state = random_state
        np.random.seed(random_state)
        random.seed(random_state)

        self.task_type = self._detect_task_type()
        self._prepare_data()
        self.is_poly_data_ = self._estimate_polynomial_nature() if self.do_polynomial_expansion else False
        self.perspectives = self._generate_perspectives_auto()

        # Add a "PERFECT_PERSPECTIVE" that uses ALL features:
        self._add_perfect_perspective()

        self.best_persp_name_ = None
        self.meta_learner_ = None

    def _detect_task_type(self):
        dtype = self.dataset[self.target].dtype
        if np.issubdtype(dtype, np.floating):
            return "regression"
        elif np.issubdtype(dtype, np.integer):
            return "classification"
        else:
            raise ValueError("Unsupported target type.")

    def _prepare_data(self):
        self.scaler_X = MinMaxScaler()
        X_raw = self.dataset[self.features].values
        self.X = self.scaler_X.fit_transform(X_raw)

        if self.task_type == "regression":
            self.scaler_y = MinMaxScaler()
            y_raw = self.dataset[[self.target]].values
            self.y = self.scaler_y.fit_transform(y_raw).flatten()
        else:
            self.y = self.dataset[self.target].astype(float).values

    def _estimate_polynomial_nature(self):
        if self.task_type != "regression":
            return False
        var_feats = np.var(self.X, axis=0)
        main_idx = np.argmax(var_feats)
        subset_size = min(200, len(self.y))
        idxs = np.random.choice(len(self.y), subset_size, replace=False)
        X_sub = ensure_2d(self.X[idxs, main_idx])
        y_sub = self.y[idxs]

        lin = LinearRegression()
        lin.fit(X_sub, y_sub)
        lin_mse = mean_squared_error(y_sub, lin.predict(X_sub))

        poly = PolynomialFeatures(degree=self.poly_degree, include_bias=False)
        X_poly_sub = poly.fit_transform(X_sub)
        lin2 = LinearRegression()
        lin2.fit(X_poly_sub, y_sub)
        poly_mse = mean_squared_error(y_sub, lin2.predict(X_poly_sub))

        ratio = (lin_mse - poly_mse) / (lin_mse + 1e-9)
        return ratio > 0.3

    def _generate_perspectives_auto(self):
        perspectives = {}
        n_feats = len(self.features)
        from sklearn.preprocessing import PolynomialFeatures

        for i in range(1, self.max_auto_perspectives + 1):
            subset_size = np.random.randint(1, n_feats + 1)
            f_indices = random.sample(range(n_feats), subset_size)

            is_poly = False
            poly_obj = None
            if (
                self.is_poly_data_
                and random.random() < 0.5
                and self.task_type == "regression"
            ):
                is_poly = True
                poly_obj = PolynomialFeatures(
                    degree=self.poly_degree, include_bias=False
                )

            if is_poly:
                X_subset = self.X[:, f_indices]
                X_poly = poly_obj.fit_transform(X_subset)
                n_cols = X_poly.shape[1]
                init_w = np.random.randn(n_cols + 1) * 0.01
                perspectives[f"Perspective_{i}"] = {
                    "features": f_indices,
                    "weights": init_w,
                    "is_poly": True,
                    "poly_obj": poly_obj,
                }
            else:
                init_w = np.random.randn(subset_size + 1) * 0.01
                perspectives[f"Perspective_{i}"] = {
                    "features": f_indices,
                    "weights": init_w,
                    "is_poly": False,
                    "poly_obj": None,
                }
        return perspectives

    def _add_perfect_perspective(self):
        """Add a 'PERFECT_PERSPECTIVE' that uses ALL features."""
        from sklearn.preprocessing import PolynomialFeatures

        all_feats_indices = list(range(len(self.features)))
        is_poly = False
        poly_obj = None
        if self.task_type == "regression" and self.is_poly_data_:
            is_poly = True
            poly_obj = PolynomialFeatures(degree=self.poly_degree, include_bias=False)
            X_all = self.X[:, all_feats_indices]
            X_poly_all = poly_obj.fit_transform(X_all)
            n_cols = X_poly_all.shape[1]
            init_w = np.random.randn(n_cols + 1) * 0.01
            self.perspectives["PERFECT_PERSPECTIVE"] = {
                "features": all_feats_indices,
                "weights": init_w,
                "is_poly": True,
                "poly_obj": poly_obj
            }
        else:
            # If classification or not polynomial data
            init_w = np.random.randn(len(self.features) + 1) * 0.01
            self.perspectives["PERFECT_PERSPECTIVE"] = {
                "features": all_feats_indices,
                "weights": init_w,
                "is_poly": False,
                "poly_obj": None
            }

    def _init_optimizer_state(self, n_w):
        self.m = np.zeros(n_w)
        self.v = np.zeros(n_w)

    def _forward_and_grad(self, X, y, w, is_poly=False, poly_obj=None):
        n = len(y)
        w_no_bias = w[:-1]
        b = w[-1]

        if self.task_type == "regression":
            preds = X @ w_no_bias + b
            loss = np.mean((preds - y) ** 2)
            grad_w = (2.0 / n) * (X.T @ (preds - y))
            grad_b = (2.0 / n) * np.sum(preds - y)
        else:  # classification
            eps = 1e-9
            logits = X @ w_no_bias + b
            preds = 1.0 / (1.0 + np.exp(-logits))
            loss = -np.mean(y * np.log(preds + eps) + (1 - y) * np.log(1 - preds + eps))
            diff = preds - y
            grad_w = (X.T @ diff) / n
            grad_b = np.mean(diff)

        grad_w += self.lambda_reg * w_no_bias
        grad = np.append(grad_w, grad_b)
        return loss, grad, preds

    def _update_weights(self, w, grad, epoch_t, weight_decay=1e-5, beta1=0.9, beta2=0.999, eps=1e-8):
        grad = np.clip(grad, -self.gradient_clip_value, self.gradient_clip_value)
        if self.optimizer == "adam":
            self.m = beta1 * self.m + (1 - beta1) * grad
            self.v = beta2 * self.v + (1 - beta2) * (grad ** 2)
            m_hat = self.m / (1 - beta1 ** epoch_t)
            v_hat = self.v / (1 - beta2 ** epoch_t)
            step = self.learning_rate * m_hat / (np.sqrt(v_hat) + eps)
            w -= step
        elif self.optimizer == "adamw":
            self.m = beta1 * self.m + (1 - beta1) * grad
            self.v = beta2 * self.v + (1 - beta2) * (grad ** 2)
            m_hat = self.m / (1 - beta1 ** epoch_t)
            v_hat = self.v / (1 - beta2 ** epoch_t)
            step = self.learning_rate * m_hat / (np.sqrt(v_hat) + eps)
            # weight decay for all but bias
            w[:-1] -= weight_decay * w[:-1]
            w -= step
        elif self.optimizer == "rmsprop":
            rho = 0.9
            self.v = rho * self.v + (1 - rho) * (grad ** 2)
            w -= self.learning_rate * grad / (np.sqrt(self.v) + eps)
        else:
            w -= self.learning_rate * grad
        return w

    def _batch_generator(self, X, y, shuffle=True):
        idxs = np.arange(len(y))
        if shuffle:
            np.random.shuffle(idxs)
        for start_idx in range(0, len(y), self.batch_size):
            end_idx = min(start_idx + self.batch_size, len(y))
            bidx = idxs[start_idx:end_idx]
            yield X[bidx], y[bidx]

    def train_perspective_cv(self, perspective):
        f_idx = perspective["features"]
        w = perspective["weights"]
        is_poly = perspective["is_poly"]
        poly_obj = perspective["poly_obj"]

        if is_poly and poly_obj is not None:
            X_sub = poly_obj.transform(self.X[:, f_idx])
        else:
            X_sub = self.X[:, f_idx]

        kf = KFold(n_splits=self.n_splits, shuffle=True, random_state=self.random_state)
        fold_losses = []
        best_loss_glob = float('inf')
        best_weights_glob = None

        for train_idx, val_idx in kf.split(X_sub):
            w_fold = np.copy(w)
            self._init_optimizer_state(len(w_fold))

            X_tr, X_val = X_sub[train_idx], X_sub[val_idx]
            y_tr, y_val = self.y[train_idx], self.y[val_idx]
            best_loss_fold = float('inf')
            best_weights_fold = np.copy(w_fold)
            wait = 0

            for epoch in range(1, self.epochs + 1):
                for bX, bY in self._batch_generator(X_tr, y_tr):
                    loss_batch, grad_batch, _ = self._forward_and_grad(bX, bY, w_fold, is_poly, poly_obj)
                    w_fold = self._update_weights(w_fold, grad_batch, epoch)

                val_loss, _, _ = self._forward_and_grad(X_val, y_val, w_fold, is_poly, poly_obj)
                if val_loss < best_loss_fold:
                    best_loss_fold = val_loss
                    best_weights_fold = np.copy(w_fold)
                    wait = 0
                else:
                    wait += 1
                    if wait >= self.patience:
                        break

            fold_losses.append(best_loss_fold)
            if best_loss_fold < best_loss_glob:
                best_loss_glob = best_loss_fold
                best_weights_glob = best_weights_fold

        avg_loss = np.mean(fold_losses)
        return avg_loss, best_weights_glob

    def train_perspectives(self):
        for nm, persp in self.perspectives.items():
            print(f"\nTraining {nm}...")
            cv_loss, best_w = self.train_perspective_cv(persp)
            persp["loss"] = cv_loss
            persp["weights"] = best_w
            print(f"{nm} CV Loss: {cv_loss:.4f}")

        best_nm = min(self.perspectives, key=lambda nm: self.perspectives[nm]["loss"])
        self.best_persp_name_ = best_nm
        print(f"\nBest Perspective by CV: {best_nm}, Loss={self.perspectives[best_nm]['loss']:.4f}")

    def refine_best_perspective(self):
        # Retrain best perspective with extended epochs
        persp = self.perspectives[self.best_persp_name_]
        f_idx = persp["features"]
        is_poly = persp["is_poly"]
        poly_obj = persp["poly_obj"]
        w = np.copy(persp["weights"])

        if is_poly and poly_obj is not None:
            X_p = poly_obj.transform(self.X[:, f_idx])
        else:
            X_p = self.X[:, f_idx]
        y_p = self.y

        val_ratio = 0.2
        split_idx = int(len(y_p) * (1 - val_ratio))
        X_tr, X_val = X_p[:split_idx], X_p[split_idx:]
        y_tr, y_val = y_p[:split_idx], y_p[split_idx:]

        self._init_optimizer_state(len(w))
        best_w = np.copy(w)
        best_loss = float('inf')
        wait = 0

        # Extended refinement epochs
        refine_epochs = 1000

        for epoch in range(1, refine_epochs + 1):
            for bX, bY in self._batch_generator(X_tr, y_tr):
                loss_b, grad_b, _ = self._forward_and_grad(bX, bY, w, is_poly, poly_obj)
                w = self._update_weights(w, grad_b, epoch)

            val_loss, _, _ = self._forward_and_grad(X_val, y_val, w, is_poly, poly_obj)
            if val_loss < best_loss:
                best_loss = val_loss
                best_w = np.copy(w)
                wait = 0
            else:
                wait += 1
                if wait >= self.patience:
                    break

        persp["weights"] = best_w
        persp["loss"] = best_loss

    def build_meta_ensemble(self):
        if len(self.perspectives) < 2:
            self.meta_learner_ = None
            print("[WARNING] Not enough perspectives to build a meta-ensemble.")
            return

        preds_for_meta = []
        for nm, persp in self.perspectives.items():
            f_idx = persp["features"]
            is_poly = persp["is_poly"]
            poly_obj = persp["poly_obj"]
            w = persp["weights"]

            if is_poly and poly_obj is not None:
                X_p = poly_obj.transform(self.X[:, f_idx])
            else:
                X_p = self.X[:, f_idx]

            if self.task_type == "regression":
                preds_ = X_p @ w[:-1] + w[-1]
            else:
                logits = X_p @ w[:-1] + w[-1]
                preds_ = 1.0 / (1.0 + np.exp(-logits))
            preds_for_meta.append(preds_.reshape(-1, 1))

        X_meta = np.concatenate(preds_for_meta, axis=1)
        y_meta = self.y

        if len(np.unique(y_meta)) < 2:
            print("[WARNING] Meta-learner skipped due to single class in y_meta.")
            self.meta_learner_ = None
            return

        if self.task_type == "regression":
            self.meta_learner_ = LinearRegression()
            self.meta_learner_.fit(X_meta, y_meta)
        else:
            self.meta_learner_ = LogisticRegression(max_iter=1000)
            self.meta_learner_.fit(X_meta, y_meta)

    def train(self):
        self.train_perspectives()
        self.refine_best_perspective()
        self.build_meta_ensemble()

    def predict(self, new_data):
        new_data_scaled = self.scaler_X.transform(new_data)
        if self.meta_learner_ is not None and len(self.perspectives) > 1:
            meta_feats = []
            for nm, persp in self.perspectives.items():
                f_idx = persp["features"]
                is_poly = persp["is_poly"]
                poly_obj = persp["poly_obj"]
                w = persp["weights"]

                if is_poly and poly_obj is not None:
                    X_sub = poly_obj.transform(new_data_scaled[:, f_idx])
                else:
                    X_sub = new_data_scaled[:, f_idx]

                if self.task_type == "regression":
                    preds_s = X_sub @ w[:-1] + w[-1]
                else:
                    logits = X_sub @ w[:-1] + w[-1]
                    preds_s = 1.0 / (1.0 + np.exp(-logits))
                meta_feats.append(preds_s.reshape(-1,1))

            X_meta = np.concatenate(meta_feats, axis=1)
            if self.task_type == "regression":
                meta_out = self.meta_learner_.predict(X_meta)
                return self.scaler_y.inverse_transform(meta_out.reshape(-1,1)).flatten()
            else:
                return self.meta_learner_.predict(X_meta)
        else:
            persp = self.perspectives[self.best_persp_name_]
            f_idx = persp["features"]
            is_poly = persp["is_poly"]
            poly_obj = persp["poly_obj"]
            w = persp["weights"]

            if is_poly and poly_obj is not None:
                X_sub = poly_obj.transform(new_data_scaled[:, f_idx])
            else:
                X_sub = new_data_scaled[:, f_idx]

            if self.task_type == "regression":
                preds_s = X_sub @ w[:-1] + w[-1]
                return self.scaler_y.inverse_transform(preds_s.reshape(-1,1)).flatten()
            else:
                logits = X_sub @ w[:-1] + w[-1]
                probs = 1.0 / (1.0 + np.exp(-logits))
                return probs