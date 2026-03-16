import Head from 'next/head';
import { GetServerSideProps } from 'next';
import { supabase } from '../lib/supabase';

interface Merchant {
  name: string;
}

interface Offer {
  id: number;
  title: string;
  price: number;
  power_kwc?: number | null;
  battery_kwh?: number | null;
  merchants?: Merchant | null;
}

interface HomeProps {
  offers: Offer[];
}

export const getServerSideProps: GetServerSideProps<HomeProps> = async () => {
  // Fetch offers with associated merchant names.  Note: requires
  // Postgres RPC row level security configured accordingly.
  const { data, error } = await supabase
    .from('offers')
    .select('id, title, price, power_kwc, battery_kwh, merchants(name)')
    .order('price', { ascending: true })
    .limit(50);

  if (error) {
    console.error('Supabase error', error);
    return { props: { offers: [] } };
  }
  return { props: { offers: data as Offer[] } };
};

export default function Home({ offers }: HomeProps) {
  return (
    <>
      <Head>
        <title>OffreSolaire – Comparateur de kits solaires</title>
        <meta
          name="description"
          content="Comparez les kits solaires plug and play selon la puissance et le prix."
        />
      </Head>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Comparateur de kits solaires</h1>
        {offers.length === 0 && (
          <p className="text-gray-600">Aucune offre disponible pour le moment.</p>
        )}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {offers.map((offer) => (
            <div
              key={offer.id}
              className="border rounded p-4 shadow-sm hover:shadow-md transition"
            >
              <h2 className="text-xl font-semibold mb-2">{offer.title}</h2>
              <p className="text-sm text-gray-500 mb-1">
                Vendeur : {offer.merchants?.name ?? 'N/A'}
              </p>
              <p className="text-lg font-bold mb-1">{offer.price.toFixed(2)} €</p>
              {offer.power_kwc && (
                <p className="text-sm text-gray-600">
                  Puissance : {offer.power_kwc} kWc
                </p>
              )}
              {offer.battery_kwh && (
                <p className="text-sm text-gray-600">
                  Batterie : {offer.battery_kwh} kWh
                </p>
              )}
            </div>
          ))}
        </div>
      </main>
    </>
  );
}