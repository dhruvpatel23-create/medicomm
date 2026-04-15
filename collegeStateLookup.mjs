const collegeStateEntries = [
  ["aiims delhi", "Delhi"],
  ["all india institute of medical sciences new delhi", "Delhi"],
  ["armed forces medical college pune", "Maharashtra"],
  ["b j medical college ahmedabad", "Gujarat"],
  ["bj medical college ahmedabad", "Gujarat"],
  ["b j government medical college pune", "Maharashtra"],
  ["bj government medical college pune", "Maharashtra"],
  ["bangalore medical college and research institute", "Karnataka"],
  ["bangalore medical college", "Karnataka"],
  ["banaras hindu university institute of medical sciences", "Uttar Pradesh"],
  ["institute of medical sciences bhu varanasi", "Uttar Pradesh"],
  ["christian medical college vellore", "Tamil Nadu"],
  ["government medical college amritsar", "Punjab"],
  ["government medical college srinagar", "Jammu and Kashmir"],
  ["grant medical college mumbai", "Maharashtra"],
  ["indira gandhi medical college shimla", "Himachal Pradesh"],
  ["jawaharlal institute of postgraduate medical education and research", "Puducherry"],
  ["jipmer puducherry", "Puducherry"],
  ["jnims imphal", "Manipur"],
  ["jawaharlal nehru institute of medical sciences imphal", "Manipur"],
  ["king georges medical university lucknow", "Uttar Pradesh"],
  ["kgmu lucknow", "Uttar Pradesh"],
  ["lady hardinge medical college new delhi", "Delhi"],
  ["madras medical college chennai", "Tamil Nadu"],
  ["madras medical college", "Tamil Nadu"],
  ["maulana azad medical college new delhi", "Delhi"],
  ["maulana azad medical college", "Delhi"],
  ["mysore medical college and research institute", "Karnataka"],
  ["mysore medical college", "Karnataka"],
  ["neigrihms shillong", "Meghalaya"],
  ["north eastern indira gandhi regional institute of health and medical sciences shillong", "Meghalaya"],
  ["osmania medical college hyderabad", "Telangana"],
  ["osmania medical college", "Telangana"],
  ["patna medical college", "Bihar"],
  ["pt b d sharma pgims rohtak", "Haryana"],
  ["pt bd sharma pgims rohtak", "Haryana"],
  ["pgims rohtak", "Haryana"],
  ["rims ranchi", "Jharkhand"],
  ["rajendra institute of medical sciences ranchi", "Jharkhand"],
  ["scb medical college cuttack", "Odisha"],
  ["sms medical college jaipur", "Rajasthan"],
  ["sawai man singh medical college jaipur", "Rajasthan"],
  ["sikkim manipal institute of medical sciences", "Sikkim"],
  ["stanley medical college chennai", "Tamil Nadu"],
  ["stanley medical college", "Tamil Nadu"],
  ["topiwala national medical college mumbai", "Maharashtra"],
  ["topiwala national medical college", "Maharashtra"],
  ["vmmc and safdarjung hospital new delhi", "Delhi"],
  ["vmmc safdarjung hospital", "Delhi"],
  ["vmmc and safdarjung hospital", "Delhi"],
  ["andhra medical college visakhapatnam", "Andhra Pradesh"],
  ["andhra medical college", "Andhra Pradesh"],
  ["trihms naharlagun", "Arunachal Pradesh"],
  ["tomo riba institute of health and medical sciences naharlagun", "Arunachal Pradesh"],
  ["assam medical college dibrugarh", "Assam"],
  ["assam medical college", "Assam"],
  ["pt jnm medical college raipur", "Chhattisgarh"],
  ["pt j n m medical college raipur", "Chhattisgarh"],
  ["goa medical college", "Goa"],
  ["government medical college thiruvananthapuram", "Kerala"],
  ["gandhi medical college bhopal", "Madhya Pradesh"],
  ["zoram medical college falkawn", "Mizoram"],
  ["naga hospital authority kohima", "Nagaland"],
  ["agartala government medical college", "Tripura"],
  ["government doon medical college dehradun", "Uttarakhand"],
  ["medical college kolkata", "West Bengal"],
  ["sal institute of medical sciences ahmedabad", "Gujarat"],
  ["sal institute of medical sciences", "Gujarat"],
];

function normalizeCollegeName(value) {
  return String(value ?? "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const collegeStateLookup = new Map(collegeStateEntries);

function resolveCollegeState(collegeName) {
  const normalized = normalizeCollegeName(collegeName);
  if (!normalized) return null;

  if (collegeStateLookup.has(normalized)) {
    return collegeStateLookup.get(normalized);
  }

  for (const [key, state] of collegeStateLookup.entries()) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return state;
    }
  }

  return null;
}

export { normalizeCollegeName, resolveCollegeState };
