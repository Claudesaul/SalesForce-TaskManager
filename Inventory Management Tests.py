import pytest
import sqlite3
import os
from Inventory_Management import Inventory, Customer, Machines


@pytest.fixture
def temp_inventory_db(tmp_path):
    db_path = os.path.join(tmp_path, 'test_inventory.db')
    inventory = Inventory(db_file=db_path)
    yield inventory
    os.remove(db_path)


def test_create_table(temp_inventory_db):
    conn = sqlite3.connect(temp_inventory_db.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None


def test_populate_inventory(temp_inventory_db):
    file_path = 'inventoryList.txt'
    temp_inventory_db.populate_inventory(file_path)
    conn = sqlite3.connect(temp_inventory_db.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventory")
    result = cursor.fetchone()[0]
    conn.close()
    assert result > 0


def test_display_inventory(capsys, temp_inventory_db):
    temp_inventory_db.display_inventory()
    captured = capsys.readouterr()

    if "Inventory is empty." not in captured.out:
        assert "ID" in captured.out
    else:
        assert "Inventory is empty." in captured.out


@pytest.fixture
def temp_customer_db(tmp_path):
    db_path = os.path.join(tmp_path, 'test_customers.db')
    customer = Customer(db_file=db_path)
    yield customer
    os.remove(db_path)


def test_create_table(temp_customer_db):
    conn = sqlite3.connect(temp_customer_db.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None


def test_populate_customers(temp_customer_db):
    file_path = 'customerList.txt'
    temp_customer_db.populate_customers(file_path)
    conn = sqlite3.connect(temp_customer_db.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    result = cursor.fetchone()[0]
    conn.close()
    assert result > 0


def test_display_customers(capsys, temp_customer_db):
    temp_customer_db.display_customers()
    captured = capsys.readouterr()
    assert captured.out.strip() == ''


def test_get_coordinates_by_id(temp_customer_db):
    customer_id = 1
    coordinates = temp_customer_db.get_coordinates_by_id(customer_id)
    assert coordinates is None


@pytest.fixture
def temp_machines_db(tmp_path):
    db_path = os.path.join(tmp_path, 'test_machines.db')
    machines = Machines(db_file=db_path)
    yield machines
    os.remove(db_path)


def test_create_table(temp_machines_db):
    conn = sqlite3.connect(temp_machines_db.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='machines'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None


def test_populate_machines(temp_machines_db):
    file_path = 'machinesList.txt'
    temp_machines_db.populate_machines(file_path)
    conn = sqlite3.connect(temp_machines_db.db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM machines")
    result = cursor.fetchone()[0]
    conn.close()
    assert result > 0


def test_display_machines(capsys, temp_machines_db):
    conn_c = sqlite3.connect(temp_machines_db.db_file)
    cursor_c = conn_c.cursor()
    cursor_c.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, coordinates TEXT)")
    conn_c.commit()
    conn_c.close()

    temp_machines_db.display_machines()
    captured = capsys.readouterr()
    assert captured.out.strip() == ''
