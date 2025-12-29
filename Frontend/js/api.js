const BASE_URL = "http://127.0.0.1:8000";

// ---------- USERS ----------
export async function registerUser(data) {
    const res = await fetch(`${BASE_URL}/users/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    return res.json();
}

export async function loginUser(data) {
    const res = await fetch(`${BASE_URL}/login/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    return res.json();
}

// ---------- PRODUCTS ----------
export async function getProducts() {
    const res = await fetch(`${BASE_URL}/products/`);
    return res.json();
}


// ---------- CART ----------
export async function addToCart(userId, productId, quantity) {
    const res = await fetch(`${BASE_URL}/users/${userId}/card`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ product_id: productId, quantity })
    });
    return res.json();
}

// ---------- WISHLIST ----------
export async function addWishlist(userId, productId) {
    const res = await fetch(`${BASE_URL}/user/${userId}/wishlist`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ product_id: productId })
    });
    return res.json();
}

export async function getWishlist(userId) {
    const res = await fetch(`${BASE_URL}/user/${userId}/wishlist`);
    return res.json();
}

// ---------- ORDERS ----------
export async function placeOrder(userId, data) {
    const res = await fetch(`${BASE_URL}/user/${userId}/order`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    return res.json();
}
