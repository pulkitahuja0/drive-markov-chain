export const downToText = (down: number) => {
	if (down == 1) return '1st';
	if (down == 2) return '2nd';
	if (down == 3) return '3rd';
	if (down == 4) return '4th';
};

export const keyToLabel = (key: string) => {
	if (key == 'touchdown') return 'Touchdown';
	if (key == 'punt') return 'Punt';
	if (key == 'turnover') return 'Turnover';
	if (key == 'bad_fg') return 'Missed/blocked Field Goal';
	if (key == 'made_fg') return 'Made Field Goal';
	if (key == 'safety') return 'Safety';
	if (key == 'turnover_on_downs') return 'Turnover on Downs';

	const [down, yardsToGo, yardsFromEndZone] = stateMatcher(key);
	return `${downToText(down)} & ${yardsToGo} ${yardsFromEndZone} yards from the end zone`;
};

export const stateMatcher = (key: string) => {
	const regex = /^(\d+(?:\.\d+)?)_(\d+(?:\.\d+)?)_(\d+(?:\.\d+)?)$/;
	const match = key.match(regex);
	if (match) {
		const [, x, y, z] = match;
		const [down, yardsToGo, yardsFromEndZone] = [x, y, z].map(Number);

		return [down, yardsToGo, yardsFromEndZone];
	} else {
		return [0, 0, 0];
	}
};

export const createKey = (down: number, yardsToGo: number, yardline: number) => {
	return `${down}.0_${yardsToGo}.0_${yardline}.0`;
};
