# **Data Warehouse Design for the IDL Project**

**Information and Communications Technologies Research Group (ICTRG)**

---

## **1. Executive Summary**

The IDL project aims to create a unified data layer and warehouse for IoT sensor data to enable scalable storage, real-time analytics, and secure access for authorized users. This report evaluates modern open-source technologies for building a data warehouse and analytics stack, proposes viable architectures, and recommends a solution optimized for IoT data volume, velocity, and variety. Key findings include:

- **ClickHouse** (columnar database) and **Apache Kafka** (streaming) are ideal for real-time IoT workloads.
- **Apache Superset** provides intuitive analytics and visualization.
- A hybrid architecture combining stream processing (Apache Flink) and batch analytics ensures flexibility.

---

## **2. Introduction**

### **2.1 Project Overview**

The IDL project involves two stages:

1. **Data Layer**: Centralized ingestion of heterogeneous IoT sensor data.
2. **Data Warehouse**: On-demand access to historical and real-time data for analytics.

### **2.2 Objectives**

- Identify open-source tools for scalable data warehousing.
- Propose integrated stacks for IoT data ingestion, storage, and analytics.
- Evaluate trade-offs between performance, scalability, and ease of use.

---

## **3. Literature Review**

### **3.1 Data Warehousing: Concepts & Evolution**

- **Traditional vs. Modern Data Warehouses and Data Lake**: The concept of the data warehouse originated in the 1990s, predating data lakes, and was initially designed to manage multiple enterprise database instances. In the early 21st century, with the explosion of the internet, big data emerged as traditional databases struggled to handle massive data volumes. Google and others established foundational frameworks for distributed storage, scheduling, and computing. By the second decade of the 21st century, big data technology matured, with user-friendly SQL-based engines making unified data warehouses a reality. Simultaneously, the concept of "data lakes" emerged with open storage and computation models. These two systems advanced on both commercial and open-source trajectories.
- **IoT-Specific Challenges**: High write throughput, time-series optimization, and horizontal scalability.

---

## **4. Technology Evaluation**

### **4.1 Data Warehousing Solutions**

| **Tool**         | **Pros**                                                    | **Cons**                                | **IoT Suitability**                                  |
| ---------------- | ----------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| **ClickHouse**   | High-speed queries, columnar storage                        | Schema rigidity, limited UPDATE support | Excellent (time-series focus)                        |
| **TimescaleDB**  | PostgreSQL compatibility, SQL-friendly                      | Scalability limits for massive datasets | Good (hybrid transactional/analytical)               |
| **Apache Doris** | MySQL protocol support, real-time updates, MPP architecture | Smaller community than ClickHouse       | Excellent (balanced real-time + batch, SQL-friendly) |

### **4.2 Data Analytics Tools**

| **Tool**            | **Pros**                                     | **Cons**                                   |
| ------------------- | -------------------------------------------- | ------------------------------------------ |
| **Apache Superset** | Rich visualizations, SQL editor, open-source | Limited alerting, moderate learning curve  |
| **Metabase**        | User-friendly, lightweight                   | Fewer advanced features (e.g., geospatial) |
| **Grafana**         | Ideal for time-series dashboards             | Tight coupling with monitoring systems     |

### **4.3 Useful Tools for Data Pipeline**

A robust data pipeline for IoT requires tools for **ingestion**, **processing**, **orchestration**, and **monitoring**. Below are key open-source tools:

- **0. Data Messaging & Ingestion**

| **Tool**         | **Description**                                                                     | **IoT Use Case**                                                 |
| ---------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Apache Kafka** | Distributed event streaming platform for high-throughput, fault-tolerant messaging. | Real-time sensor data ingestion, decoupling producers/consumers. |
| **Redpanda**     | Kafka-compatible, ZooKeeper-free streaming. Simpler deployment.                     | Edge IoT scenarios with limited resources.                       |

- **1. Stream Processing & Real-Time ETL**

| **Tool**         | **Description**                                                             | **IoT Use Case**                                         |
| ---------------- | --------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Apache Flink** | Stateful stream processing with low latency. Supports event-time semantics. | Real-time anomaly detection, windowed aggregations.      |
| **Apache Spark** | Batch & streaming processing. Ideal for ML integration (Spark MLlib).       | Large-scale batch ETL (e.g., historical data backfills). |
| **Apache Beam**  | Unified API for batch/streaming. Runs on Flink, Spark, etc.                 | Portable pipelines across cloud/on-prem.                 |

- **2. Workflow Orchestration**

| **Tool**           | **Description**                                 | **IoT Use Case**                          |
| ------------------ | ----------------------------------------------- | ----------------------------------------- |
| **Apache Airflow** | Python-based DAG scheduler for batch workflows. | Scheduling ETL jobs, sensor data backups. |

- **3. Lightweight Data Collection**

| **Tool**       | **Description**                                                            | **IoT Use Case**              |
| -------------- | -------------------------------------------------------------------------- | ----------------------------- |
| **Telegraf**   | Agent-based metrics collector (part of TICK stack). Supports 200+ plugins. | Pulling sensor data from MQTT |
| **Fluent Bit** | Lightweight log processor/forwarder. Low resource footprint.               | Edge device log aggregation.  |

- **4. Monitoring & Observability**

| **Tool**       | **Description**                                            | **IoT Use Case**                            |
| -------------- | ---------------------------------------------------------- | ------------------------------------------- |
| **Prometheus** | Time-series monitoring with alerting. Pull-based scraping. | Tracking sensor health metrics.             |
| **Grafana**    | Visualization for Prometheus, InfluxDB, etc.               | Dashboards for temperature/humidity trends. |

- **5. Distributed Query Engines**

| **Tool**  | **Description**                                                    | **IoT Use Case**                                        |
| --------- | ------------------------------------------------------------------ | ------------------------------------------------------- |
| **Trino** | Federated SQL engine (query across databases). Formerly PrestoSQL. | Joining IoT data with business data (e.g., PostgreSQL). |

---

## **5. Proposed Architectures**

![diagram](../IDL-NBCC/Screenshot/iot_pipeline_with_clickhouse_data_warehouse%201.png)

### **5.1 Recommended Stack: Real-Time IoT Analytics**

[](https://via.placeholder.com/600x400?text=IoT+Sensors-%3EKafka-%3EFlink-%3EClickHouse-%3ESuperset)

**Components**:

1. **Ingestion**: Apache Kafka for streaming sensor data.
2. **Processing**: Apache Flink for filtering, aggregation, and anomaly detection.
3. **Storage**: ClickHouse for low-latency OLAP queries.
4. **Analytics**: Apache Superset for dashboards and ad-hoc SQL.

### **5.2 Alternative Stack: Batch-Hybrid Approach**

**Tools**: Apache Spark (batch processing) + TimescaleDB + Metabase.

---

## **6. Evaluation & Trade-Offs**

| **Criteria**          | **Kafka + Flink + ClickHouse** | **Spark + TimescaleDB**        |
| --------------------- | ------------------------------ | ------------------------------ |
| **Latency**           | Real-time (ms)                 | Near-real-time (minutes)       |
| **Scalability**       | Petabyte-scale                 | TB-scale                       |
| **Ease of Use**       | Moderate (requires DevOps)     | High (SQL-centric)             |
| **Community Support** | Strong (Apache projects)       | Growing (PostgreSQL ecosystem) |

---

## **Appendices**

- ### **Appendix A**: Glossary of Terms

  - **<a id="Zookeeper"></a>Zookeeper**:
    Apache ZooKeeper is a distributed coordination service used to manage and synchronize large-scale distributed systems. It provides a centralized service for tasks like maintaining configuration information, naming, distributed synchronization, and group services. Commonly used in distributed applications like Kafka and Hadoop.

  - **<a id="MPP"></a>MPP**: Massively Parallel Processing MPP is a computing architecture where multiple processors work on different parts of a task simultaneously. MPP databases (e.g., Greenplum, ClickHouse) distribute data and processing across multiple nodes to achieve high performance for large-scale data analytics.

  - **<a id="OLAP"></a>OLAP**: OLAP(Online Analytical Processing) refers to systems designed for complex queries and data analysis. OLAP databases (e.g., Apache Druid, StarRocks)

  - **<a id="OLTP"></a>OLTP**: OLTP refers to systems designed for transactional workloads, such as inserting, updating, and deleting small amounts of data. OLTP databases (e.g., PostgreSQL)

  - **<a id="CDC"></a>CDC**: (Change Data Capture)CDC is a technique for tracking and capturing changes in a database (e.g., inserts, updates, deletes) in real time. It is often used for data replication, synchronization, and ETL processes to ensure data consistency across systems.

  - **<a id="ETL"></a>ETL**: (Extract, Transform, Load)ETL is a data integration process where data is extracted from source systems, transformed into a usable format, and loaded into a target database or data warehouse. It is a key component of data pipelines and analytics workflows.

- ### **Appendix B**: Sample Queries & Screenshots.

  ![ClickHouse install](../IDL-NBCC/Screenshot/ClickhouseInstalled.png)
  ![ClickHouse Table](../IDL-NBCC/Screenshot/TableCreated_SoundLevel.png)
  ![ClickHouse Query](../IDL-NBCC/Screenshot/QuerySample_Clickhouse.png)

- ### **Appendix C**: Full List of Reviewed Data Warehouse.

#### **1. Core Positioning & Use Cases**

| **System**     | **Core Focus**                             | **Use Cases**                                                                               |
| -------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Hive**       | Hadoop-based offline data warehouse        | Large-scale batch ETL, offline analytics (e.g., log processing, data lake storage)          |
| **Druid**      | Real-time time-series analytics            | Real-time monitoring, ad analytics, user behavior analysis (low latency + high concurrency) |
| **ClickHouse** | High-performance OLAP columnar database    | Wide-table aggregations, log/behavioral analytics (extremely fast single-table queries)     |
| **Kudu**       | Real-time updatable storage engine         | Real-time data updates + analysis (e.g., IoT sensor data, financial transactions)           |
| **Greenplum**  | Enterprise MPP data warehouse              | Complex ETL, business intelligence (BI), hybrid workloads (PostgreSQL-compatible)           |
| **Pinot**      | Low-latency real-time OLAP engine          | Interactive real-time analytics (e.g., clickstream analysis, like LinkedIn's use case)      |
| **PostgreSQL** | General-purpose RDBMS (supports OLTP/OLAP) | Transaction processing, medium-scale analytics (with extensions like TimescaleDB)           |
| **StarRocks**  | High-performance MPP OLAP engine           | High-concurrency real-time analytics, ad-hoc queries (e.g., e-commerce dashboards)          |
| **Doris**      | Lightweight MPP OLAP engine                | Real-time reporting, mid-scale analytics (simplified fork of StarRocks)                     |

---

#### **2. Architecture & Performance**

| **System**     | **Storage Model**             | **Query Latency** | **Throughput** | **Scalability**                   | **Real-time Ingestion** |
| -------------- | ----------------------------- | ----------------- | -------------- | --------------------------------- | ----------------------- |
| **Hive**       | Row/Column (ORC)              | Minutes           | High           | High (via HDFS)                   | No (batch-only)         |
| **Druid**      | Columnar + inverted index     | Sub-second        | Medium         | High (distributed)                | Yes (streaming)         |
| **ClickHouse** | Columnar                      | Seconds           | Very High      | Moderate (sharding via ZooKeeper) | Yes (batch/stream)      |
| **Kudu**       | Columnar                      | Seconds           | High           | High (distributed)                | Yes (real-time updates) |
| **Greenplum**  | Row/Columnar                  | Minutes           | High           | Moderate (MPP scaling)            | Yes (batch)             |
| **Pinot**      | Columnar + inverted index     | Sub-second        | High           | High (auto-sharding)              | Yes (streaming)         |
| **PostgreSQL** | Row-based (column extensions) | Seconds-minutes   | Medium         | Limited (replication)             | Yes (transactional)     |
| **StarRocks**  | Columnar                      | Sub-second        | Very High      | High (elastic)                    | Yes (streaming)         |
| **Doris**      | Columnar                      | Seconds           | High           | High (distributed)                | Yes (batch/stream)      |

---

#### **3. Key Features**

| **System**     | **Strengths**                         | **Weaknesses**                                              | **Data Updates**    | **Transactions**    |
| -------------- | ------------------------------------- | ----------------------------------------------------------- | ------------------- | ------------------- |
| **Hive**       | SQL compatibility, mature ecosystem   | High latency, not for interactive                           | Overwrite-only      | No                  |
| **Druid**      | Low latency, high concurrency         | Complex pre-aggregation, weak joins                         | No                  | No                  |
| **ClickHouse** | Blazing-fast scans, high compression  | Poor multi-table joins, no transactions                     | Limited (via ALTER) | No                  |
| **Kudu**       | Real-time updates, Hadoop integration | Limited storage scale, needs compute engines (e.g., Impala) | Yes                 | Partial (row-level) |
| **Greenplum**  | Complex query optimization, ACID      | Costly scaling, weak real-time                              | Yes                 | Yes (full ACID)     |
| **Pinot**      | Fast multi-dimensional aggregations   | Complex setup, smaller community                            | No                  | No                  |
| **PostgreSQL** | Versatile, extensible                 | Performance degrades at scale                               | Yes                 | Yes (OLTP)          |
| **StarRocks**  | High concurrency, vectorized engine   | Young ecosystem, fewer optimizations                        | Yes                 | Partial (batch)     |
| **Doris**      | Simple setup, MySQL compatibility     | Fewer features vs. StarRocks                                | Yes                 | Partial (batch)     |

---

#### **4. Open-source version vs Paid versions**

| **Tool/Project** | **Open-Source Status**                                             | **Paid Version/Commercial Support**                                                        | **Key Differences Between Free and Paid**                                                                                 |
| ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| **Apache Hive**  | Fully open-source (Apache 2.0 License)                             | No official paid version, but third-party commercial support (e.g., Cloudera, Hortonworks) | Free version is fully functional; paid support offers enterprise services (e.g., technical support, optimization)         |
| **Apache Druid** | Fully open-source (Apache 2.0 License)                             | Commercial versions available (e.g., Imply, CelerData)                                     | Free version is fully functional; commercial versions offer enhanced features (e.g., management tools, support)           |
| **ClickHouse**   | Fully open-source (Apache 2.0 License)                             | Commercial version (ClickHouse Cloud)                                                      | Free version is fully functional; commercial version offers managed services, management, and support                     |
| **Apache Kudu**  | Fully open-source (Apache 2.0 License)                             | No official paid version, but third-party commercial support (e.g., Cloudera)              | Free version is fully functional; paid support offers enterprise services                                                 |
| **Greenplum**    | Open-source (Apache 2.0 License)                                   | Commercial version (VMware Tanzu Greenplum)                                                | Free version is fully functional; commercial version offers advanced features and support                                 |
| **Apache Pinot** | Fully open-source (Apache 2.0 License)                             | Commercial versions available (e.g., StarTree)                                             | Free version is fully functional; commercial versions offer extended features and managed services                        |
| **PostgreSQL**   | Fully open-source (PostgreSQL License)                             | Commercial support available (e.g., EnterpriseDB)                                          | Free version is fully functional; commercial versions offer advanced features, support, and management tools              |
| **StarRocks**    | Partially open-source (Community Edition under Apache 2.0 License) | Commercial version (StarRocks Enterprise)                                                  | Community Edition has limited features; Enterprise Edition offers more features (e.g., data security, cluster management) |
| **Apache Doris** | Fully open-source (Apache 2.0 License)                             | Commercial support available (e.g., CelerData)                                             | Free version is fully functional; commercial versions offer extended features and support                                 |

- ### **References**:
  - Benchmarking Tools: [ClickHouse Benchmark](https://benchmark.clickhouse.com/)
  - Ecosystem Rankings: [Database Ranking](https://benchant.com/ranking/database-ranking)

---
