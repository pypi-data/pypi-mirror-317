-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
--@ Join table matching freight shipments and deliveries

CREATE TABLE Freight_Shipment_Delivery (
    "shipment_id"  INTEGER NOT NULL,    --@ Shipment id (foreign key to freight_shipment table)
    "tour_id"      INTEGER NOT NULL,    --@ Tour id (foreign key to freight_delivery table)
    "leg_id"       INTEGER NOT NULL, --@ Leg id in a tour (foreign key to freight_delivery table)

    PRIMARY KEY (shipment_id, tour_id, leg_id)

)