import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const hgetAsync = promisify(client.hget).bind(client);

const listProducts = [
    { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
    { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
    { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
    { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Function to get an item by ID from listProducts
const getItemById = (id) => {
    return listProducts.find(item => item.itemId === id);
};

// Reserve stock by item ID
const reserveStockById = (itemId, stock) => {
    client.set(`item.${itemId}`, stock);
};

// Get current reserved stock by item ID
const getCurrentReservedStockById = async (itemId) => {
    const reservedStock = await getAsync(`item.${itemId}`);
    return reservedStock ? parseInt(reservedStock) : 0;
};

// Route to list all products
app.get('/list_products', (req, res) => {
    res.json(listProducts.map(item => ({
        itemId: item.itemId,
        itemName: item.itemName,
        price: item.price,
        initialAvailableQuantity: item.initialAvailableQuantity
    })));
});

// Route to get product details by item ID
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const item = getItemById(itemId);
    if (!item) {
        return res.json({ status: 'Product not found' });
    }
    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({
        itemId: item.itemId,
        itemName: item.itemName,
        price: item.price,
        initialAvailableQuantity: item.initialAvailableQuantity,
        currentQuantity: currentQuantity
    });
});

// Route to reserve a product by item ID
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId);
    const item = getItemById(itemId);
    if (!item) {
        return res.json({ status: 'Product not found' });
    }
    const currentQuantity = await getCurrentReservedStockById(itemId);
    if (currentQuantity >= item.initialAvailableQuantity) {
        return res.json({ status: 'Not enough stock available', itemId: itemId });
    }
    reserveStockById(itemId, currentQuantity + 1);
    res.json({ status: 'Reservation confirmed', itemId: itemId });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
