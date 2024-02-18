{{ config(materialized='table') }}

select      ACCESSIONNUMBER     as accession_number
            , FILE_NUM          as file_num
            , case
                when regexp_contains(FILING_DATE, r'[A-Za-z]') then
                    parse_date('%d-%b-%Y', FILING_DATE)
                else
                    cast(FILING_DATE as datetime)
            end                 as filing_datetime
            , SIC_CODE          as sic_code
            , SCHEMAVERSION     as schema_version
            , SUBMISSIONTYPE    as submission_type
            , TESTORLIVE        as test_or_live
            , case
                when coalesce(OVER100PERSONSFLAG, '') = 'true' then
                    true
                when OVER100PERSONSFLAG is null then
                    null
            end                 as over_100_persons_flag
            , case
                when coalesce(OVER100ISSUERFLAG, '') = 'true' then
                    true
                when OVER100ISSUERFLAG is null then
                    null
            end                 as over_100_issuer_flag
from        {{ source('raw', 'submissions')}}
