resource "aws_glue_catalog_database" "reddit" {
  name = "reddit"
}

resource "aws_glue_catalog_table" "reddit-threads" {
  name          = "threads"
  database_name = aws_glue_catalog_database.reddit.name

  table_type = "EXTERNAL_TABLE"

  partition_keys {
    name = "year"
    type = "int"
  }

  partition_keys {
    name = "month"
    type = "int"
  }

  partition_keys {
    name = "day"
    type = "int"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/threads/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "title"
      type = "string"
    }

    columns {
      name = "selftext"
      type = "string"
    }

    columns {
      name = "author"
      type = "string"
    }

    columns {
      name = "permalink"
      type = "string"
    }

    columns {
      name = "comments"
      type = "int"
    }

    columns {
      name = "upvotes"
      type = "int"
    }

    columns {
      name = "downvotes"
      type = "int"
    }

    columns {
      name = "created"
      type = "bigint"
    }

  }

  parameters = {
    "projection.enabled"        = "true"
    "projection.year.type"      = "integer"
    "projection.year.range"     = "2025,2050"
    "projection.month.type"     = "integer"
    "projection.month.range"    = "1,12"
    "projection.day.type"       = "integer"
    "projection.day.range"      = "1,31"
    "storage.location.template" = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/threads/year=$${year}/month=$${month}/day=$${day}/"
    "EXTERNAL"                  = "TRUE"
  }
}


resource "aws_glue_catalog_table" "reddit-comments" {
  name          = "comments"
  database_name = aws_glue_catalog_database.reddit.name

  table_type = "EXTERNAL_TABLE"

  partition_keys {
    name = "year"
    type = "int"
  }

  partition_keys {
    name = "month"
    type = "int"
  }

  partition_keys {
    name = "day"
    type = "int"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/comments/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "thread_id"
      type = "string"
    }

    columns {
      name = "text"
      type = "string"
    }

    columns {
      name = "author"
      type = "string"
    }

    columns {
      name = "permalink"
      type = "string"
    }

    columns {
      name = "upvotes"
      type = "int"
    }

    columns {
      name = "downvotes"
      type = "int"
    }

    columns {
      name = "created"
      type = "bigint"
    }

  }

  parameters = {
    "projection.enabled"        = "true"
    "projection.year.type"      = "integer"
    "projection.year.range"     = "2025,2050"
    "projection.month.type"     = "integer"
    "projection.month.range"    = "1,12"
    "projection.day.type"       = "integer"
    "projection.day.range"      = "1,31"
    "storage.location.template" = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/comments/year=$${year}/month=$${month}/day=$${day}/"
    "EXTERNAL"                  = "TRUE"
  }
}


resource "aws_glue_catalog_table" "subreddits" {
  name          = "subreddits"
  database_name = aws_glue_catalog_database.reddit.name

  table_type = "EXTERNAL_TABLE"

  partition_keys {
    name = "year"
    type = "int"
  }

  partition_keys {
    name = "month"
    type = "int"
  }

  partition_keys {
    name = "day"
    type = "int"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/subreddits/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "name"
      type = "string"
    }

    columns {
      name = "subscribers"
      type = "int"
    }


  }

  parameters = {
    "projection.enabled"        = "true"
    "projection.year.type"      = "integer"
    "projection.year.range"     = "2025,2050"
    "projection.month.type"     = "integer"
    "projection.month.range"    = "1,12"
    "projection.day.type"       = "integer"
    "projection.day.range"      = "1,31"
    "storage.location.template" = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/subreddits/year=$${year}/month=$${month}/day=$${day}/"
    "EXTERNAL"                  = "TRUE"
  }
}
