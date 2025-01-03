uint64_t GetMortonCode(const Eigen::Vector3f& max, const Eigen::Vector3f& min, int maxDepth, const Eigen::Vector3f& position)
{
	// Validate and compute range
	Eigen::Vector3f range = max - min;
	range = range.cwiseMax(Eigen::Vector3f::Constant(1e-6f)); // Avoid zero range

	// Normalize position
	Eigen::Vector3f relativePos = (position - min).cwiseQuotient(range);

	// Clamp to [0, 1]
	relativePos = relativePos.cwiseMax(0.0f).cwiseMin(1.0f);

	// Scale to Morton grid size
	uint32_t maxCoordinateValue = (1 << maxDepth) - 1;
	uint32_t x = static_cast<uint32_t>(relativePos.x() * maxCoordinateValue);
	uint32_t y = static_cast<uint32_t>(relativePos.y() * maxCoordinateValue);
	uint32_t z = static_cast<uint32_t>(relativePos.z() * maxCoordinateValue);
	
	// Compute Morton code
	uint64_t mortonCode = 0;
	for (int i = 0; i < maxDepth; ++i) {
		mortonCode |= ((x >> i) & 1ULL) << (3 * i);
		mortonCode |= ((y >> i) & 1ULL) << (3 * i + 1);
		mortonCode |= ((z >> i) & 1ULL) << (3 * i + 2);
	}

	return mortonCode;
}
