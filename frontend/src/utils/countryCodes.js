import * as countryCodesList from "country-codes-list";

export const isoToFlag = (iso) =>
  iso
    .toUpperCase()
    .replace(/./g, (char) => String.fromCodePoint(127397 + char.charCodeAt(0)));

const rawList = countryCodesList.customList(
  "countryCode",
  "{countryNameEn}|+{countryCallingCode}",
);

export const countryList = Object.entries(rawList)
  .map(([iso, entry]) => {
    const [label, code] = entry.split("|");
    return { iso, code, label, flag: isoToFlag(iso) };
  })
  .filter((c) => c.code !== "+")
  .sort((a, b) => {
    if (a.iso === "IN") return -1;
    if (b.iso === "IN") return 1;
    return a.label.localeCompare(b.label);
  });

export const splitPhone = (fullPhone) => {
  if (!fullPhone) return { countryCode: "+91", number: "" };

  const sortedByCodeLength = [...countryList].sort(
    (a, b) => b.code.length - a.code.length,
  );

  const match = sortedByCodeLength.find((c) => fullPhone.startsWith(c.code));

  if (!match) {
    return { countryCode: "+91", number: fullPhone.replace(/^\+/, "") };
  }

  return { countryCode: match.code, number: fullPhone.slice(match.code.length) };
};