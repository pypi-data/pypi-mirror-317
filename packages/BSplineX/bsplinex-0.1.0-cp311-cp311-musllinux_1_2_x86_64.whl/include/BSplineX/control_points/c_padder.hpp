#ifndef C_PADDER_HPP
#define C_PADDER_HPP

// Standard includes
#include <stdexcept>
#include <vector>

// BSplineX includes
#include "BSplineX/control_points/c_data.hpp"
#include "BSplineX/defines.hpp"
#include "BSplineX/types.hpp"

namespace bsplinex::control_points
{

template <typename T, BoundaryCondition BC>
class Padder
{
public:
  Padder() = default;

  Padder(Data<T> &, size_t) {}

  T right(size_t) const
  {
    throw std::runtime_error(
        "Generic control points padder has zero length, this function is here only for "
        "compatibility reasons."
    );
  }

  [[nodiscard]] size_t size() const { return 0; }

  [[nodiscard]] size_t size_right() const { return 0; }
};

template <typename T>
class Padder<T, BoundaryCondition::PERIODIC>
{
private:
  std::vector<T> pad_right{};

public:
  Padder() = default;

  Padder(Data<T> &data, size_t degree) { this->pad_right = data.slice(0, degree); }

  T right(size_t index) const
  {
    assertm(index < this->pad_right.size(), "Out of bounds");
    return this->pad_right[index];
  }

  [[nodiscard]] size_t size() const { return this->pad_right.size(); }

  [[nodiscard]] size_t size_right() const { return this->pad_right.size(); }
};

} // namespace bsplinex::control_points

#endif
