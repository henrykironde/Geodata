SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
CREATE TABLE "nuclear"."shp" (gid serial,
"id" numeric(10,0),
"name" varchar(80));
ALTER TABLE "nuclear"."shp" ADD PRIMARY KEY (gid);
SELECT AddGeometryColumn('nuclear','shp','geom','0','POINT',2);
INSERT INTO "nuclear"."shp" ("id","name",geom) VALUES ('1','Sellafield','0101000000FE53435AFFF80BC0E00C43FBCC354B40');
CREATE INDEX ON "nuclear"."shp" USING GIST ("geom");
COMMIT;
