CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE profiles (
    profile_id TEXT PRIMARY KEY,
    float_file TEXT,
    date_time TIMESTAMP WITH TIME ZONE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    geom GEOMETRY(Point, 4326),
    ocean TEXT,
    institution TEXT,
    profiler_type TEXT,
    summary TEXT,
    argo_index_row_id INT
);

CREATE INDEX idx_profiles_geom ON profiles USING GIST(geom);
CREATE INDEX idx_profiles_date ON profiles(date_time);