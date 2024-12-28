# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md

from polaris.utils.database.db_utils import drop_table, has_table
from polaris.utils.database.standard_database import DatabaseType, StandardDatabase


def migrate(conn):
    db = StandardDatabase.for_type(DatabaseType.Demand)
    if has_table(conn, "freight_delivery"):
        drop_table(conn, "freight_delivery")
    if has_table(conn, "freight_shipment"):
        drop_table(conn, "freight_shipment")
    if has_table(conn, "freight_shipment_delivery"):
        drop_table(conn, "freight_shipment_delivery")

    db.add_table(conn, "freight_delivery", None, add_defaults=False)
    db.add_table(conn, "freight_shipment", None, add_defaults=False)
    db.add_table(conn, "freight_shipment_delivery", None, add_defaults=False)
