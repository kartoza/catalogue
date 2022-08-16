BEGIN;

ALTER TABLE dictionaries_spectralmodeprocessingcosts ADD CONSTRAINT "dictionaries_spectralmodeprocessingcosts_currency_id_fkey" FOREIGN KEY (currency_id) REFERENCES exchange_currency(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE orders_nonsearchrecord ADD CONSTRAINT "orders_nonsearchrecord_currency_id_fkey" FOREIGN KEY (currency_id) REFERENCES exchange_currency(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE search_searchrecord ADD CONSTRAINT "search_searchrecord_currency_id_fkey" FOREIGN KEY (currency_id) REFERENCES exchange_currency(id) DEFERRABLE INITIALLY DEFERRED;

COMMIT;
