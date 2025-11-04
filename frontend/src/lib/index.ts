const downToText = (down: number) => {
	if (down == 1) return '1st';
	if (down == 2) return '2nd';
	if (down == 3) return '3rd';
	if (down == 4) return '4th';
};

const keyToLabel = (key: string) => {
	if (key == 'touchdown') return 'Touchdown';
	if (key == 'punt') return 'Punt';
	if (key == 'turnover') return 'Turnover';
	if (key == 'bad_fg') return 'Missed/blocked Field Goal';
	if (key == 'made_fg') return 'Made Field Goal';

	const regex = /^(\d+(?:\.\d+)?)_(\d+(?:\.\d+)?)_(\d+(?:\.\d+)?)$/;
	const match = key.match(regex);
	if (match) {
		const [, x, y, z] = match;
		const [down, yardsToGo, yardline] = [x, y, z].map(Number);

		return `${downToText(down)} & ${yardsToGo} at the ${yardline}`;
	}
};
