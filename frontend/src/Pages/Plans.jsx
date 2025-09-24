export default function Plans() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Available Plans</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 border rounded-xl shadow hover:shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Daily Plan</h2>
          <p>Access for 24 hours</p>
          <p className="mt-2 font-bold">$1</p>
          <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            Subscribe
          </button>
        </div>
        <div className="p-6 border rounded-xl shadow hover:shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Weekly Plan</h2>
          <p>Access for 7 days</p>
          <p className="mt-2 font-bold">$5</p>
          <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            Subscribe
          </button>
        </div>
        <div className="p-6 border rounded-xl shadow hover:shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Monthly Plan</h2>
          <p>Access for 30 days</p>
          <p className="mt-2 font-bold">$15</p>
          <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            Subscribe
          </button>
        </div>
      </div>
    </div>
  );
}
