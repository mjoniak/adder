from collections import namedtuple
from unittest import TestCase

from connector import Connector

Point = namedtuple('Point', ['x', 'y'])


def create_connector(x=10, y=20):
    conn = Connector(x, y)
    return conn


class ConnectorTest(TestCase):
    def test_connect(self):
        first_conn = create_connector()
        second_conn = create_connector()
        first_conn.connect_with(second_conn)
        self.assertIn(second_conn, first_conn.connections)

    def test_contains_borders(self):
        conn = create_connector(0, 0)
        self.assertTrue(conn.contains(Point(0, 0)))
        self.assertTrue(conn.contains(Point(conn.width, 0)))
        self.assertTrue(conn.contains(Point(0, conn.height)))
        self.assertTrue(conn.contains(Point(conn.width, conn.height)))

    def test_does_not_contain_outside(self):
        conn = create_connector(0, 0)
        self.assertFalse(conn.contains(Point(conn.width + 1, 0)))
